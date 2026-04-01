#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive News Aggregator for Subway Safety Monitoring
=========================================================

Core Value: Real-time search and aggregation of subway safety incidents,
regulations, technology updates, and industry news from multiple sources.

Key Features:
- Multi-source web scraping with anti-bot measures
- RSS feed aggregation via RSSHub
- WeChat/Weibo monitoring with alternative methods
- Scheduled automated updates
- Content filtering and deduplication

Anti-Scraping Solutions:
1. User-Agent rotation
2. Request delays and rate limiting
3. Proxy rotation support
4. Cookie handling
5. Headless browser simulation
6. RSS feeds as alternative when direct scraping fails
"""

import requests
import json
import logging
import time
import random
import re
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class NewsItem:
    """Represents a single news item"""

    title: str
    url: str
    source: str
    publish_date: str = ""
    summary: str = ""
    category: str = "news"  # safety, law, news, technology
    verified: bool = False
    scrape_time: str = field(default_factory=lambda: datetime.now().isoformat())
    keywords: List[str] = field(default_factory=list)
    content_hash: str = ""


class AntiBotConfig:
    """Configuration for anti-bot measures"""

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]

    DELAY_RANGE = (2, 5)  # Random delay between requests
    RETRY_COUNT = 3
    TIMEOUT = 30

    @classmethod
    def get_random_ua(cls) -> str:
        return random.choice(cls.USER_AGENTS)


class RSSFeedAggregator:
    """
    RSS feed aggregator using RSSHub
    RSSHub creates RSS feeds for many websites that don't have native RSS
    """

    RSSHUB_INSTANCES = [
        "https://rsshub.app",
        "https://api.rsshub.app",
        "https://rss.bnu.edu.cn",
    ]

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": AntiBotConfig.get_random_ua(),
                "Accept": "application/rss+xml, application/xml, text/xml, */*",
            }
        )
        self.fallback_instance_idx = 0

    def _get_next_rsshub(self) -> str:
        """Cycle through RSSHub instances"""
        instance = self.RSSHUB_INSTANCES[self.fallback_instance_idx]
        self.fallback_instance_idx = (self.fallback_instance_idx + 1) % len(
            self.RSSHUB_INSTANCES
        )
        return instance

    def fetch_rss(self, url: str, topic: str = "") -> List[Dict]:
        """
        Fetch and parse RSS feed

        Args:
            url: The RSS feed URL
            topic: Topic identifier for logging

        Returns:
            List of parsed feed items
        """
        items = []

        for attempt in range(3):
            try:
                rsshub = self._get_next_rsshub()
                feed_url = f"{rsshub}/{url}" if not url.startswith("http") else url

                response = self.session.get(feed_url, timeout=AntiBotConfig.TIMEOUT)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "xml")
                    for entry in soup.find_all("item")[:20]:
                        item = self._parse_entry(entry, topic)
                        if item:
                            items.append(item)
                    break
                elif response.status_code == 404:
                    logger.warning(f"RSS feed not found: {feed_url}")
                    break

            except Exception as e:
                logger.warning(
                    f"RSS fetch attempt {attempt + 1} failed for {topic}: {str(e)[:50]}"
                )
                time.sleep(2)

        return items

    def _parse_entry(self, entry, source: str) -> Optional[Dict]:
        """Parse a single RSS entry"""
        try:
            title = entry.title.text if entry.title else ""
            link = entry.link.text if entry.link else ""
            pub_date = entry.pubDate.text if entry.pubDate else ""
            description = ""
            if entry.description:
                desc_text = entry.description.text or ""
                description = re.sub(r"<[^>]+>", "", desc_text)[:500]

            return {
                "title": title.strip(),
                "url": link.strip(),
                "source": source,
                "publish_date": pub_date.strip(),
                "summary": description.strip(),
            }
        except Exception as e:
            logger.debug(f"Failed to parse RSS entry: {e}")
            return None

    def fetch_weibo_user(self, uid: str, source_name: str) -> List[Dict]:
        """Fetch Weibo user timeline via RSS"""
        return self.fetch_rss(f"weibo/user/{uid}", source_name)

    def fetch_weibo_search(self, keyword: str) -> List[Dict]:
        """Search Weibo by keyword via RSS"""
        encoded_kw = quote(keyword)
        return self.fetch_rss(f"weibo/search/{encoded_kw}", f"Weibo搜索:{keyword}")

    def fetch_rss_feed(self, feed_path: str, source_name: str) -> List[Dict]:
        """Generic RSS feed fetcher"""
        return self.fetch_rss(feed_path, source_name)


class WeChatCollector:
    """
    WeChat Official Account data collector

    WeChat has no public API, so we use alternative methods:
    1. Sogou WeChat search (limited but free)
    2. Third-party data platforms (require API keys)
    3. Manual data import via CSV
    """

    SOGOU_SEARCH_URL = "https://weixin.sogou.com/weixin"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": AntiBotConfig.get_random_ua(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )

    def search_wechat_articles(
        self, keywords: List[str], max_results: int = 10
    ) -> List[Dict]:
        """
        Search WeChat articles via Sogou search

        Note: This is limited - Sogou only returns recent articles
        and may require CAPTCHA for heavy usage
        """
        articles = []

        for keyword in keywords[:5]:  # Limit searches
            try:
                search_url = f"{self.SOGOU_SEARCH_URL}?type=2&s_from=input&query={quote(keyword)}&ie=utf8&_sug_=n&_sug_type_="

                response = self.session.get(search_url, timeout=AntiBotConfig.TIMEOUT)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    results = soup.select(".news-box .news-list li")

                    for item in results[:max_results]:
                        article = self._parse_sogou_result(item, keyword)
                        if article:
                            articles.append(article)

                time.sleep(random.uniform(3, 6))

            except Exception as e:
                logger.warning(f"WeChat search failed for '{keyword}': {str(e)[:50]}")

        return articles

    def _parse_sogou_result(self, item, keyword: str) -> Optional[Dict]:
        """Parse a Sogou WeChat search result"""
        try:
            title_elem = item.select_one(".txt h3 a") or item.select_one(".title a")
            if not title_elem:
                return None

            title = title_elem.get_text().strip()
            url = title_elem.get("href", "")

            date_elem = item.select_one(".s2") or item.select_one(".time")
            date = date_elem.get_text().strip() if date_elem else ""

            source_elem = item.select_one(".s1") or item.select_one(".account")
            source = source_elem.get_text().strip() if source_elem else ""

            return {
                "title": title,
                "url": url,
                "source": f"WeChat:{source}" if source else "WeChat",
                "publish_date": date,
                "summary": f"关键词: {keyword}",
                "platform": "wechat",
            }
        except Exception:
            return None


class ContentClassifier:
    """Classify news content into categories"""

    EXCLUDE_KEYWORDS = [
        "会议",
        "座谈会",
        "研讨会",
        "论坛",
        "年会",
        "博览会",
        "展览会",
        "签约",
        "会见",
        "拜访",
        "访问",
        "考察",
        "参观",
        "开幕",
        "闭幕",
        "致辞",
        "讲话",
        "发言",
        "代表",
        "领导",
        "考察团",
        "代表团",
        "出席",
        "参加",
        "参会",
        "参展",
        "开幕词",
        "闭幕词",
        "合影",
        "颁奖",
        "授牌",
        "挂牌",
        "成立大会",
        "换届",
        "选举",
        "任命",
        "董事",
        "总经理",
        "副总裁",
        "副主任",
        "主任",
        "会长",
        "副会长",
        "秘书长",
        "理事长",
        "exhibition",
        "conference",
        "forum",
        "summit",
        "visit",
        "meeting",
        "ceremony",
    ]

    CATEGORIES = {
        "safety": [
            "安全",
            "事故",
            "险性",
            "事件",
            "故障",
            "延误",
            "中断",
            "紧急",
            "救援",
            "injury",
            "accident",
            "emergency",
            "incident",
            "safety",
            "collision",
            "撞人",
            "脱轨",
            "火灾",
            "塌方",
            "溺水",
            "伤亡",
            "急救",
            "抢救",
            "闯入",
            "停车",
            "停运",
            "延误",
            "晚点",
            "冒烟",
            "停电",
            "停水",
            "塌陷",
            "坠落",
            "乘客",
            "伤亡",
        ],
        "law": [
            "法规",
            "条例",
            "规定",
            "办法",
            "标准",
            "规范",
            "政策",
            "发布",
            "law",
            "regulation",
            "policy",
            "standard",
            "issued",
            "amendment",
            "交通运输部",
            "住建部",
            "发改委",
            "应急管理部",
            "通知",
            "GB ",
            "TB ",
            "CJ ",
            "建标",
            "发布",
            "批准",
            "施行",
            "修订",
            "征求意见",
            "公示",
        ],
        "technology": [
            "创新",
            "技术",
            "系统",
            "升级",
            "改造",
            "technology",
            "innovation",
            "system",
            "upgrade",
            "AI",
            "无人驾驶",
            "全自动运行",
            "FAO",
            "云平台",
            "大数据",
            "人工智能",
            "智能运维",
            "智慧地铁",
            "5G",
            "车车通信",
            "自主运行",
            "信号系统",
            "屏蔽门",
            "新技术",
            "新突破",
            "首试",
            "首次",
            "突破",
        ],
        "operation": [
            "开通",
            "试运行",
            "开通运营",
            "列车",
            "地铁",
            "轨道",
            "operation",
            "metro",
            "subway",
            "rail",
            "service",
            "line",
            "发车",
            "停运",
            "运行",
            "首班车",
            "末班车",
            "新线",
            "开工",
            "在建",
            "建成",
            "投入运营",
            "联调联试",
            "空载",
            "试运营",
            "初期运营",
            "竣工",
            "验收",
        ],
    }

    @classmethod
    def should_exclude(cls, title: str, summary: str = "") -> bool:
        """Check if content should be excluded based on negative keywords"""
        text = (title + " " + summary).lower()
        for kw in cls.EXCLUDE_KEYWORDS:
            if kw.lower() in text:
                return True
        return False

    @classmethod
    def classify(cls, title: str, summary: str = "") -> str:
        """Classify content into category"""
        if cls.should_exclude(title, summary):
            return "exclude"

        text = (title + " " + summary).lower()

        scores = {}
        for category, keywords in cls.CATEGORIES.items():
            score = sum(1 for kw in keywords if kw.lower() in text)
            scores[category] = score

        if max(scores.values()) == 0:
            return "news"

        return max(scores, key=scores.get)

    @classmethod
    def extract_keywords(cls, title: str, summary: str = "") -> List[str]:
        """Extract relevant keywords from content"""
        text = title + " " + summary
        keywords = []

        for category, kw_list in cls.CATEGORIES.items():
            for kw in kw_list:
                if kw.lower() in text.lower():
                    if kw not in keywords:
                        keywords.append(kw)

        return keywords[:10]


class DirectWebScraper:
    """
    Direct web scraper for authoritative government and metro websites.
    Bypasses RSSHub for more reliable data collection.
    """

    AUTHORITATIVE_SOURCES = [
        {
            "name": "交通运输部",
            "url": "https://www.mot.gov.cn/",
            "section": "交通运输部",
            "selectors": {
                "items": ".news-list li, .article-list li, .list-item",
                "title": "a",
                "date": ".date, .time",
            },
            "relevant_keywords": [
                "安全",
                "地铁",
                "轨道",
                "运营",
                "应急",
                "管理",
                "办法",
                "规定",
                "标准",
                "规范",
                "通知",
            ],
        },
        {
            "name": "中国城市轨道交通协会",
            "url": "https://www.camet.org.cn/sy/xydt/",
            "section": "行业动态",
            "selectors": {
                "items": ".main-item",
                "title": ".content-title",
                "date": ".content-time .time",
                "link": ".detail_box",
            },
            "relevant_keywords": [
                "安全",
                "运营",
                "开通",
                "开工",
                "建设",
                "技术",
                "创新",
                "设备",
                "标准",
                "规范",
                "演练",
                "故障",
                "事故",
                "新线",
                "轨 道",
                "地铁",
            ],
        },
        {
            "name": "国家铁路局",
            "url": "https://www.nra.gov.cn/",
            "section": "国家铁路局",
            "selectors": {
                "items": ".news-list li, .article-list li",
                "title": "a",
                "date": ".date",
            },
            "relevant_keywords": [
                "安全",
                "铁路",
                "监管",
                "规定",
                "办法",
                "标准",
                "通知",
                "处罚",
            ],
        },
        {
            "name": "应急管理部",
            "url": "https://www.mem.gov.cn/",
            "section": "应急管理部",
            "selectors": {
                "items": ".news-list li, .article-list li",
                "title": "a",
                "date": ".date",
            },
            "relevant_keywords": [
                "安全",
                "应急",
                "事故",
                "救援",
                "灾害",
                "预警",
            ],
        },
    ]

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": AntiBotConfig.get_random_ua(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a single page"""
        try:
            response = self.session.get(url, timeout=AntiBotConfig.TIMEOUT)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding or "utf-8"
                return response.text
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {str(e)[:50]}")
        return None

    def scrape_source(self, source: Dict) -> List[Dict]:
        """Scrape a single authoritative source"""
        items = []
        html = self.fetch_page(source["url"])
        if not html:
            return items

        try:
            soup = BeautifulSoup(html, "html.parser")
            item_elements = soup.select(source["selectors"]["items"])

            for elem in item_elements[:20]:
                try:
                    title_elem = elem.select_one(source["selectors"]["title"])
                    if not title_elem:
                        continue

                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue

                    link_elem = elem.select_one(source["selectors"].get("link", "a"))
                    url = ""
                    if link_elem:
                        url = link_elem.get("href", "") or link_elem.get(
                            "data-link", ""
                        )
                    if not url:
                        url = title_elem.get("href", "")
                    if url and not url.startswith("http"):
                        url = urljoin(source["url"], url)

                    date_elem = elem.select_one(source["selectors"]["date"])
                    date = ""
                    if date_elem:
                        date_text = date_elem.get_text().strip()
                        date = re.sub(r"日期：?", "", date_text).strip()

                    text_for_check = title + source.get("section", "")
                    if not any(
                        kw in text_for_check
                        for kw in source.get("relevant_keywords", [])
                    ):
                        continue

                    items.append(
                        {
                            "title": title[:200],
                            "url": url,
                            "source": source["name"],
                            "publish_date": date,
                            "summary": f"来源: {source['name']}。分类: {source.get('section', '')}",
                        }
                    )
                except Exception:
                    continue

        except Exception as e:
            logger.warning(f"Failed to parse {source['name']}: {str(e)[:50]}")

        return items

    def scrape_all(self) -> List[Dict]:
        """Scrape all authoritative sources"""
        all_items = []
        for source in self.AUTHORITATIVE_SOURCES:
            logger.info(f"Direct scraping: {source['name']}")
            items = self.scrape_source(source)
            all_items.extend(items)
            time.sleep(random.uniform(2, 4))

        return all_items


class SummaryGenerator:
    """Generate concise summaries for news items"""

    @staticmethod
    def generate_summary(
        title: str, source: str, category: str, keywords: List[str]
    ) -> str:
        """Generate a ~500 character summary based on title and metadata"""
        summaries = {
            "safety": f"【安全事件】{source}发布安全相关信息。关键词: {', '.join(keywords[:5])}。请访问原文获取详细信息。",
            "law": f"【法规标准】{source}发布法规政策文件。关键词: {', '.join(keywords[:5])}。请访问原文获取详细信息。",
            "technology": f"【技术创新】{source}报道技术进展。关键词: {', '.join(keywords[:5])}。请访问原文获取详细信息。",
            "operation": f"【运营动态】{source}发布运营相关信息。关键词: {', '.join(keywords[:5])}。请访问原文获取详细信息。",
            "news": f"【行业动态】{source}报道: {title}。关键词: {', '.join(keywords[:5])}。请访问原文获取详细信息。",
        }
        return summaries.get(category, summaries["news"])

    @classmethod
    def enhance_news_item(cls, item: NewsItem) -> NewsItem:
        """Enhance a NewsItem with a generated summary"""
        if not item.summary or len(item.summary) < 20:
            item.summary = cls.generate_summary(
                item.title, item.source, item.category, item.keywords
            )
        return item


class MultiSourceScraper:
    """
    Main scraper class that coordinates multiple data sources
    """

    def __init__(self):
        self.rss = RSSFeedAggregator()
        self.wechat = WeChatCollector()
        self.direct = DirectWebScraper()
        self.classifier = ContentClassifier()
        self.session = requests.Session()
        self.seen_hashes = set()
        self.news_items: List[NewsItem] = []
        self.lock = threading.Lock()

        # Statistics
        self.stats = {
            "total_collected": 0,
            "sources_tried": 0,
            "successful_sources": 0,
            "start_time": None,
        }

    def _random_delay(self):
        """Apply random delay between requests"""
        delay = random.uniform(*AntiBotConfig.DELAY_RANGE)
        time.sleep(delay)

    def _update_headers(self):
        """Update session headers with new User-Agent"""
        self.session.headers.update(
            {
                "User-Agent": AntiBotConfig.get_random_ua(),
            }
        )

    def fetch_government_sources(self) -> List[NewsItem]:
        """
        Fetch news from government sources

        Government websites often have anti-scraping measures,
        so we try multiple approaches
        """
        items = []

        # Key government sources for subway safety
        sources = [
            {
                "name": "交通运输部",
                "url": "https://www.mot.gov.cn",
                "rss_path": "gov/mot",
                "selectors": ["#news-list a", ".article-list a", ".policy-list a"],
            },
            {
                "name": "应急管理部",
                "url": "https://www.mem.gov.cn",
                "rss_path": "gov/mem",
                "selectors": [".news-list a", ".article a"],
            },
            {
                "name": "国家铁路局",
                "url": "https://www.nra.gov.cn",
                "rss_path": "gov/nra",
                "selectors": [".list-item a", ".news a"],
            },
            {
                "name": "中国城市轨道交通协会",
                "url": "http://www.camet.org.cn",
                "rss_path": "gov/camet",
                "selectors": [".news-list a", ".article-list a", "ul li a"],
            },
        ]

        for source in sources:
            self.stats["sources_tried"] += 1
            try:
                # Try direct scrape first
                news = self._scrape_with_fallback(source)
                if news:
                    items.extend(news)
                    self.stats["successful_sources"] += 1
                else:
                    # Try RSS as fallback
                    news = self.rss.fetch_rss_feed(source["rss_path"], source["name"])
                    for n in news:
                        items.append(self._dict_to_newsitem(n))

                self._random_delay()

            except Exception as e:
                logger.warning(f"Failed to fetch {source['name']}: {str(e)[:50]}")

        return items

    def _scrape_with_fallback(self, source: Dict) -> List[NewsItem]:
        """Try direct scrape with anti-bot measures, fallback to RSS"""
        items = []

        for attempt in range(2):
            try:
                self._update_headers()
                response = self.session.get(
                    source["url"], timeout=AntiBotConfig.TIMEOUT, allow_redirects=True
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")

                    for selector in source.get("selectors", []):
                        elements = soup.select(selector)
                        if elements:
                            for elem in elements[:15]:
                                item = self._parse_element(elem, source["name"])
                                if item:
                                    items.append(item)
                            break

                    if items:
                        return items

                elif response.status_code in [403, 418]:
                    # Bot detected, try RSS instead
                    logger.info(
                        f"Direct access blocked for {source['name']}, using RSS fallback"
                    )
                    break

            except Exception as e:
                logger.debug(f"Attempt {attempt + 1} failed: {str(e)[:50]}")
                time.sleep(3)

        return items

    def _parse_element(self, elem, source_name: str) -> Optional[NewsItem]:
        """Parse HTML element to NewsItem"""
        try:
            # Get title
            title_elem = (
                elem
                if elem.name in ["a", "h1", "h2", "h3"]
                else elem.find(["a", "h1", "h2", "h3", "span", "p"])
            )
            if not title_elem:
                return None

            title = title_elem.get_text().strip()
            if len(title) < 10:
                return None

            # Get URL
            if elem.name == "a":
                url = elem.get("href", "")
            else:
                link_elem = elem.find("a")
                url = link_elem.get("href", "") if link_elem else ""

            if url and not url.startswith("http"):
                url = urljoin(source.get("url", ""), url)

            # Generate content hash for deduplication
            content_hash = hashlib.md5(title.encode()).hexdigest()
            if content_hash in self.seen_hashes:
                return None
            self.seen_hashes.add(content_hash)

            # Classify
            category = self.classifier.classify(title)
            keywords = self.classifier.extract_keywords(title)

            return NewsItem(
                title=title[:200],
                url=url,
                source=source_name,
                category=category,
                verified=True,
                keywords=keywords,
                content_hash=content_hash,
            )
        except Exception:
            return None

    def fetch_social_media(self, weibo_accounts: List[Dict]) -> List[NewsItem]:
        """
        Fetch social media updates via RSSHub
        """
        items = []

        for account in weibo_accounts:
            if not account.get("uid") or account["uid"] in ["", "待补充"]:
                continue

            self.stats["sources_tried"] += 1
            try:
                posts = self.rss.fetch_weibo_user(account["uid"], account["name"])

                for post in posts:
                    news_item = self._dict_to_newsitem(post)
                    if news_item:
                        items.append(news_item)

                self._random_delay()
                self.stats["successful_sources"] += 1

            except Exception as e:
                logger.warning(
                    f"Weibo fetch failed for {account['name']}: {str(e)[:50]}"
                )

        return items

    def fetch_keyword_alerts(self, keywords: List[str]) -> List[NewsItem]:
        """
        Search for content matching safety-related keywords
        """
        items = []

        for keyword in keywords[:10]:  # Limit keyword searches
            try:
                # Search via Sogou for WeChat content
                wechat_results = self.wechat.search_wechat_articles(
                    [keyword], max_results=5
                )
                for result in wechat_results:
                    news_item = self._dict_to_newsitem(result)
                    if news_item:
                        items.append(news_item)

                # Also search Weibo
                weibo_results = self.rss.fetch_weibo_search(keyword)
                for result in weibo_results:
                    news_item = self._dict_to_newsitem(result)
                    if news_item:
                        items.append(news_item)

                time.sleep(random.uniform(5, 10))

            except Exception as e:
                logger.warning(f"Keyword search failed for '{keyword}': {str(e)[:50]}")

        return items

    def _dict_to_newsitem(self, data: Dict) -> Optional[NewsItem]:
        """Convert dictionary to NewsItem with classification"""
        try:
            title = data.get("title", "")
            if not title or len(title) < 5:
                return None

            content_hash = hashlib.md5(title.encode()).hexdigest()
            if content_hash in self.seen_hashes:
                return None
            self.seen_hashes.add(content_hash)

            category = self.classifier.classify(title, data.get("summary", ""))
            keywords = self.classifier.extract_keywords(title, data.get("summary", ""))

            return NewsItem(
                title=title[:200],
                url=data.get("url", ""),
                source=data.get("source", ""),
                publish_date=data.get("publish_date", ""),
                summary=data.get("summary", "")[:500],
                category=category,
                verified=data.get("verified", False),
                keywords=keywords,
                content_hash=content_hash,
            )
        except Exception:
            return None

    def collect_all(self, weibo_accounts: List[Dict] = None) -> List[NewsItem]:
        """
        Main collection method - fetches from all sources

        Args:
            weibo_accounts: List of Weibo account dicts with 'uid' and 'name'
        """
        self.stats["start_time"] = datetime.now()
        all_items = []

        logger.info("=" * 60)
        logger.info("Starting comprehensive news collection")
        logger.info("=" * 60)

        # 1. Direct authoritative sources (most reliable)
        logger.info("Fetching from authoritative government sources...")
        try:
            direct_items = self.direct.scrape_all()
            for item_data in direct_items:
                news_item = self._dict_to_newsitem(item_data)
                if news_item:
                    all_items.append(news_item)
        except Exception as e:
            logger.warning(f"Direct scraping failed: {str(e)[:50]}")

        # 2. Government sources via RSS
        logger.info("Fetching government sources...")
        all_items.extend(self.fetch_government_sources())

        # 3. Social media via RSS
        if weibo_accounts:
            logger.info(f"Fetching {len(weibo_accounts)} Weibo accounts...")
            all_items.extend(self.fetch_social_media(weibo_accounts))

        # 4. Keyword-based search
        safety_keywords = [
            "地铁安全",
            "轨道交通事故",
            "地铁延误",
            "城市轨道交通安全",
            "metro safety incident",
            "subway emergency",
            "轨道交通 开通",
            "地铁 新线",
            "轨道 事故",
        ]
        logger.info("Searching for safety-related content...")
        all_items.extend(self.fetch_keyword_alerts(safety_keywords))

        # Deduplicate
        seen_urls = set()
        unique_items = []
        for item in all_items:
            if item.url and item.url not in seen_urls:
                seen_urls.add(item.url)
                unique_items.append(item)

        # Filter out excluded items
        filtered_items = [item for item in unique_items if item.category != "exclude"]

        # Enhance summaries
        for item in filtered_items:
            SummaryGenerator.enhance_news_item(item)

        self.news_items = filtered_items
        self.stats["total_collected"] = len(filtered_items)

        logger.info("=" * 60)
        logger.info(
            f"Collection complete: {len(filtered_items)} unique items (filtered from {len(unique_items)})"
        )
        logger.info(f"Sources tried: {self.stats['sources_tried']}")
        logger.info(f"Successful: {self.stats['successful_sources']}")
        logger.info("=" * 60)

        return unique_items

    def export_to_json(self, filename: str = None) -> str:
        """Export collected news to JSON file"""
        if filename is None:
            filename = (
                f"news_aggregated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        data = {
            "collected_at": datetime.now().isoformat(),
            "statistics": self.stats,
            "total_items": len(self.news_items),
            "items": [asdict(item) for item in self.news_items],
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Exported to {filename}")
        return filename

    def export_for_frontend(self, filename: str = "news_for_frontend.json") -> str:
        """
        Export in format compatible with frontend
        """
        events = []

        for item in self.news_items:
            events.append(
                {
                    "id": hash(item.content_hash) % 100000,
                    "time": item.publish_date[:10]
                    if item.publish_date
                    else datetime.now().strftime("%Y-%m-%d"),
                    "title": item.title,
                    "source": item.source,
                    "category": item.category,
                    "url": item.url,
                    "isNew": False,
                    "summary": item.summary
                    or f"来源: {item.source}。关键词: {', '.join(item.keywords[:5])}",
                    "verified": item.verified,
                }
            )

        data = {
            "updated_at": datetime.now().isoformat(),
            "events": events,
            "total": len(events),
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Frontend data exported to {filename}")
        return filename


def main():
    """Main execution"""
    print("=" * 70)
    print("Subway Safety News Aggregator - Multi-Source Collection System")
    print("=" * 70)
    print()
    print("Core Features:")
    print("  1. Government websites (MOT, Emergency Management, etc.)")
    print("  2. Industry associations (CAMET)")
    print("  3. Weibo via RSSHub RSS feeds")
    print("  4. WeChat via Sogou search (limited)")
    print("  5. Keyword-based alerts")
    print()
    print("Anti-Scraping Measures:")
    print("  - User-Agent rotation")
    print("  - Request delays")
    print("  - Multiple RSSHub instances")
    print("  - RSS fallback when direct access blocked")
    print()
    print("=" * 70)

    # Initialize scraper
    scraper = MultiSourceScraper()

    # Sample Weibo accounts (replace with actual from config)
    weibo_accounts = [
        {"name": "交通运输部", "uid": "2123436703"},
        {"name": "中国城市轨道交通协会", "uid": "1921971483"},
        {"name": "应急管理部", "uid": "6286498603"},
    ]

    # Collect news
    news_items = scraper.collect_all(weibo_accounts=weibo_accounts)

    # Export data
    scraper.export_to_json("scraped_news.json")
    scraper.export_for_frontend("news_for_frontend.json")

    print("\nSample of collected news:")
    for item in news_items[:5]:
        print(f"  [{item.category}] {item.title[:50]}... - {item.source}")

    return news_items


if __name__ == "__main__":
    main()
