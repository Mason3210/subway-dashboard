#!/usr/bin/env python3
"""
GitHub Actions 定时爬虫 - 自动更新地铁安全资讯
每天北京时间 8:00 自动运行
"""

import os
import re
import json
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("缺少依赖，跳过爬取")
    requests = None

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
INDEX_FILE = 'index.html'

DATA_SOURCES = [
    {'name': '交通运输部', 'url': 'https://www.mot.gov.cn/jiaotongyaowen/', 'category': 'law'},
    {'name': '北京地铁', 'url': 'https://www.bjsubway.cn/xwzx/gsxw/', 'category': 'safety'},
    {'name': '上海地铁', 'url': 'https://www.shmetro.com/node/clan/clanlist?cat=6', 'category': 'safety'},
    {'name': '广州地铁', 'url': 'https://www.gzmtr.cn/xxgk/xxgk/', 'category': 'safety'},
    {'name': '深圳地铁', 'url': 'https://www.szmc.cn/news/public', 'category': 'safety'},
    {'name': '成都地铁', 'url': 'https://www.chengdurail.com/sitegdzsxx.html', 'category': 'safety'},
    {'name': '应急管理部', 'url': 'https://www.mem.gov.cn/xw/ztzl/', 'category': 'law'},
    {'name': '中国城市轨道交通协会', 'url': 'http://www.camet.org.cn/xwdt/', 'category': 'news'},
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def fetch_news():
    """从各数据源抓取新闻"""
    news_items = []
    
    if not requests:
        return news_items
    
    for source in DATA_SOURCES:
        try:
            print(f"抓取: {source['name']}")
            response = requests.get(source['url'], headers=HEADERS, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            
            links = soup.find_all('a', href=True)
            for link in links[:5]:
                title = link.get_text(strip=True)
                if title and len(title) > 5:
                    href = link.get('href', '')
                    if href and not href.startswith('#'):
                        if not href.startswith('http'):
                            continue
                        today = datetime.now().strftime('%Y-%m-%d')
                        news_items.append({
                            'time': today,
                            'title': title[:100],
                            'source': source['name'],
                            'category': source['category'],
                            'url': href if href.startswith('http') else source['url'],
                            'isNew': True
                        })
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(f"  抓取失败: {source['name']} - {e}")
            continue
    
    return news_items


def load_existing_events():
    """从 index.html 加载已有事件"""
    if not os.path.exists(INDEX_FILE):
        return []
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'events:\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        return []
    
    events_str = match.group(1)
    events = []
    
    event_matches = re.findall(r'\{([^}]+)\}', events_str)
    for em in event_matches:
        event = {}
        for field in ['id', 'time', 'title', 'source', 'category', 'url', 'isNew']:
            m = re.search(f'{field}:\s*([^,}]+)', em)
            if m:
                value = m.group(1).strip().strip("'\"")
                if field == 'id':
                    event[field] = int(value)
                elif field == 'isNew':
                    event[field] = value == 'true'
                else:
                    event[field] = value
        if event:
            events.append(event)
    
    return events


def save_events(events):
    """保存事件到 index.html"""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_events_json = json.dumps(events[:60], ensure_ascii=False, indent=None)
    new_events_json = new_events_json.replace('true', 'true').replace('false', 'false')
    
    pattern = r'events:\s*\[.*?\]'
    content = re.sub(pattern, f'events: {new_events_json}', content, flags=re.DOTALL)
    
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = re.sub(r"lastUpdated:\s*'[^']*'", f"lastUpdated: '{today}'", content)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已更新 index.html，共 {len(events)} 条事件")


def main():
    print("="*50)
    print("开始每日地铁安全资讯更新")
    print("="*50)
    
    new_news = fetch_news()
    print(f"抓取到 {len(new_news)} 条新新闻")
    
    existing_events = load_existing_events()
    existing_ids = {e['id'] for e in existing_events}
    
    max_id = max([e['id'] for e in existing_events], default=0)
    for news in new_news:
        if news['url'] not in [e.get('url', '') for e in existing_events]:
            max_id += 1
            news['id'] = max_id
            existing_events.insert(0, news)
    
    for e in existing_events:
        e['isNew'] = False
    
    new_count = min(5, len(new_news))
    for i in range(new_count):
        if i < len(existing_events):
            existing_events[i]['isNew'] = True
    
    save_events(existing_events)
    print("更新完成!")


if __name__ == '__main__':
    main()