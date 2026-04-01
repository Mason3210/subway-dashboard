#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WeChat (微信公众号) Data Collection Module
==========================================

WeChat Official Accounts have NO public API. This module provides
multiple alternative approaches to access WeChat content:

1. Sogou WeChat Search (free, limited)
2. RSSHub WeChat RSS feeds (free, requires RSSHub deployment)
3. Third-party data platforms (paid API keys required)
4. Manual CSV import template

IMPORTANT: For production use, consider these services:
- 新榜 (xinbang.com) - WeChat data API
- 西瓜数据 (xgdata.cn) - WeChat analytics
- 清博数据 (gsdata.cn) - WeChat account analysis
- 蝉妈妈 (chanmama.com) - WeChat video analysis
"""

import requests
import json
import logging
import time
import random
import re
import csv
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import quote
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeChatCollector:
    """
    WeChat data collector with multiple fallback methods
    """

    # Sogou WeChat search
    SOGOU_BASE = "https://weixin.sogou.com/weixin"

    # Alternative: Use RSSHub if you deploy your own instance
    RSSHUB_WEIXIN = "https://rsshub.app/weixin"

    # Search keywords for safety-related content
    SAFETY_KEYWORDS = [
        "地铁安全",
        "轨道交通安全",
        "地铁事故",
        "地铁事件",
        "地铁故障",
        "地铁延误",
        "地铁中断",
        "地铁紧急",
        "地铁救援",
        "地铁应急",
        "城市轨道交通",
        "地铁运营",
        "地铁设备",
        "地铁信号",
        "地铁供电",
        "metro safety",
        "subway accident",
        "metro emergency",
    ]

    def __init__(self):
        self.session = requests.Session()
        self._update_headers()

    def _update_headers(self):
        """Update headers to mimic browser"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]
        self.session.headers.update(
            {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def search_articles(
        self, keywords: List[str] = None, max_per_keyword: int = 10
    ) -> List[Dict]:
        """
        Search WeChat articles via Sogou

        Args:
            keywords: List of keywords to search
            max_per_keyword: Maximum articles per keyword

        Returns:
            List of article dictionaries
        """
        if keywords is None:
            keywords = self.SAFETY_KEYWORDS

        all_articles = []

        for keyword in keywords[:10]:  # Limit to prevent rate limiting
            try:
                articles = self._search_single_keyword(keyword, max_per_keyword)
                all_articles.extend(articles)
                logger.info(f"Found {len(articles)} articles for keyword: {keyword}")

                # Random delay to avoid rate limiting
                time.sleep(random.uniform(3, 7))

            except Exception as e:
                logger.warning(f"Search failed for '{keyword}': {str(e)[:60]}")

        # Deduplicate by URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article["url"] not in seen_urls:
                seen_urls.add(article["url"])
                unique_articles.append(article)

        return unique_articles

    def _search_single_keyword(self, keyword: str, max_results: int) -> List[Dict]:
        """
        Search single keyword via Sogou
        """
        articles = []

        search_url = f"{self.SOGOU_BASE}?type=2&s_from=input&query={quote(keyword)}&ie=utf8&_sug_=n&_sug_type_="

        try:
            response = self.session.get(search_url, timeout=30)

            if response.status_code != 200:
                return articles

            soup = BeautifulSoup(response.content, "html.parser")

            # Parse search results
            items = soup.select(".news-box .news-list li")

            for item in items[:max_results]:
                article = self._parse_result_item(item, keyword)
                if article:
                    articles.append(article)

            # Check if CAPTCHA is required
            if soup.select(".captcha"):
                logger.warning("CAPTCHA required by Sogou. Try again later or use VPN.")

        except Exception as e:
            logger.warning(f"Sogou search error: {str(e)[:60]}")

        return articles

    def _parse_result_item(self, item, keyword: str) -> Optional[Dict]:
        """Parse a single search result item"""
        try:
            # Title and URL
            title_elem = item.select_one(".txt h3 a") or item.select_one(".title a")
            if not title_elem:
                return None

            title = title_elem.get_text().strip()
            url = title_elem.get("href", "")

            # Make URL absolute
            if url.startswith("//"):
                url = "https:" + url

            # Date
            date_elem = item.select_one(".s2") or item.select_one(".time")
            date = date_elem.get_text().strip() if date_elem else ""

            # Source account
            source_elem = item.select_one(".s1") or item.select_one(".account")
            source = source_elem.get_text().strip() if source_elem else ""

            # Description
            desc_elem = item.select_one(".txt p") or item.select_one(".description")
            description = desc_elem.get_text().strip()[:300] if desc_elem else ""

            return {
                "title": title,
                "url": url,
                "source": source or "微信公众号",
                "publish_date": date,
                "summary": description,
                "keyword": keyword,
                "platform": "wechat",
                "collected_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.debug(f"Parse error: {e}")
            return None

    def fetch_by_rss(self, account_id: str) -> List[Dict]:
        """
        Fetch WeChat articles via RSSHub

        Requires: Deploy your own RSSHub instance for reliability
        Public instances may be rate-limited or blocked
        """
        articles = []

        try:
            url = f"{self.RSSHUB_WEIXIN}/mp/{account_id}"
            response = self.session.get(url, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "xml")
                for entry in soup.find_all("item")[:10]:
                    article = {
                        "title": entry.title.text if entry.title else "",
                        "url": entry.link.text if entry.link else "",
                        "source": account_id,
                        "publish_date": entry.pubDate.text if entry.pubDate else "",
                        "platform": "wechat",
                        "collected_at": datetime.now().isoformat(),
                    }
                    articles.append(article)

        except Exception as e:
            logger.warning(f"RSS fetch failed for {account_id}: {str(e)[:60]}")

        return articles

    def fetch_by_accounts(self, accounts: List[Dict]) -> List[Dict]:
        """
        Fetch from multiple WeChat accounts

        Args:
            accounts: List of dicts with 'id' (WeChat account ID)
        """
        all_articles = []

        for account in accounts:
            account_id = account.get("id", "")
            if not account_id:
                continue

            articles = self.fetch_by_rss(account_id)
            all_articles.extend(articles)

            time.sleep(random.uniform(2, 5))

        return all_articles

    def export_to_csv(
        self, articles: List[Dict], filename: str = "wechat_articles.csv"
    ):
        """Export articles to CSV for manual review"""
        if not articles:
            logger.warning("No articles to export")
            return filename

        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "title",
                    "url",
                    "source",
                    "publish_date",
                    "summary",
                    "keyword",
                    "platform",
                    "collected_at",
                ],
            )
            writer.writeheader()
            writer.writerows(articles)

        logger.info(f"Exported {len(articles)} articles to {filename}")
        return filename

    def export_sample_csv(self, filename: str = "wechat_import_template.csv"):
        """Export sample CSV template for manual data import"""
        sample_data = [
            {
                "title": "示例：地铁安全检查通知",
                "url": "https://mp.weixin.qq.com/s/example",
                "source": "地铁公司",
                "publish_date": "2026-03-31",
                "summary": "地铁公司开展安全检查的通知详情...",
                "keyword": "安全检查",
                "platform": "wechat",
                "collected_at": datetime.now().isoformat(),
            }
        ]
        return self.export_to_csv(sample_data, filename)


class WeiboCollector:
    """
    Weibo data collector using RSSHub
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
                "User-Agent": "Mozilla/5.0 (compatible; RSSHub Bot)",
                "Accept": "application/rss+xml, application/xml, text/xml, */*",
            }
        )
        self.current_rsshub_idx = 0

    def _get_rsshub_url(self) -> str:
        """Get next RSSHub instance in rotation"""
        url = self.RSSHUB_INSTANCES[self.current_rsshub_idx]
        self.current_rsshub_idx = (self.current_rsshub_idx + 1) % len(
            self.RSSHUB_INSTANCES
        )
        return url

    def fetch_user_timeline(self, uid: str, username: str = "") -> List[Dict]:
        """
        Fetch Weibo user timeline via RSS
        """
        posts = []

        for attempt in range(3):
            try:
                rsshub = self._get_rsshub_url()
                url = f"{rsshub}/weibo/user/{uid}"

                response = self.session.get(url, timeout=30)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "xml")

                    for entry in soup.find_all("item")[:20]:
                        post = {
                            "title": entry.title.text if entry.title else "",
                            "url": entry.link.text if entry.link else "",
                            "source": username or uid,
                            "publish_date": entry.pubDate.text if entry.pubDate else "",
                            "platform": "weibo",
                            "collected_at": datetime.now().isoformat(),
                        }
                        posts.append(post)
                    break

                elif response.status_code == 404:
                    logger.warning(f"Weibo user not found: {uid}")
                    break

            except Exception as e:
                logger.warning(
                    f"Weibo fetch attempt {attempt + 1} failed: {str(e)[:50]}"
                )
                time.sleep(2)

        return posts

    def fetch_user_search(self, keyword: str, username: str = "") -> List[Dict]:
        """
        Search Weibo by keyword via RSS
        """
        posts = []

        for attempt in range(3):
            try:
                rsshub = self._get_rsshub_url()
                url = f"{rsshub}/weibo/search/{quote(keyword)}"

                response = self.session.get(url, timeout=30)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "xml")

                    for entry in soup.find_all("item")[:20]:
                        post = {
                            "title": entry.title.text if entry.title else "",
                            "url": entry.link.text if entry.link else "",
                            "source": f"微博搜索:{keyword}",
                            "publish_date": entry.pubDate.text if entry.pubDate else "",
                            "platform": "weibo",
                            "collected_at": datetime.now().isoformat(),
                        }
                        posts.append(post)
                    break

            except Exception as e:
                logger.warning(
                    f"Weibo search attempt {attempt + 1} failed: {str(e)[:50]}"
                )
                time.sleep(2)

        return posts

    def fetch_multiple_users(self, accounts: List[Dict]) -> List[Dict]:
        """
        Fetch from multiple Weibo accounts
        """
        all_posts = []

        for account in accounts:
            uid = account.get("uid", "")
            name = account.get("name", "")

            if not uid or uid in ["", "待补充"]:
                continue

            posts = self.fetch_user_timeline(uid, name)
            all_posts.extend(posts)

            time.sleep(random.uniform(2, 4))

        return all_posts

    def export_to_csv(self, posts: List[Dict], filename: str = "weibo_posts.csv"):
        """Export Weibo posts to CSV"""
        if not posts:
            logger.warning("No posts to export")
            return filename

        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "title",
                    "url",
                    "source",
                    "publish_date",
                    "platform",
                    "collected_at",
                ],
            )
            writer.writeheader()
            writer.writerows(posts)

        logger.info(f"Exported {len(posts)} posts to {filename}")
        return filename


def main():
    """Test and demonstrate capabilities"""
    print("=" * 70)
    print("Social Media Data Collection - WeChat & Weibo")
    print("=" * 70)
    print()
    print("WeChat Collection Methods:")
    print("  1. Sogou Search (free, limited by CAPTCHA)")
    print("  2. RSSHub RSS (free, requires deployment for reliability)")
    print("  3. Third-party APIs (paid: 新榜, 西瓜数据, etc.)")
    print()
    print("Weibo Collection Methods:")
    print("  1. RSSHub RSS (free, multiple instances)")
    print("  2. Weibo Search RSS")
    print()
    print("=" * 70)

    # Test WeChat search
    print("\n[Testing WeChat Search]")
    wechat = WeChatCollector()

    test_keywords = ["地铁安全", "轨道交通"]
    articles = wechat.search_articles(test_keywords, max_per_keyword=5)

    print(f"Found {len(articles)} articles")
    for article in articles[:3]:
        print(f"  - {article['title'][:50]}...")
        print(f"    Source: {article['source']} | Date: {article['publish_date']}")

    # Export template
    wechat.export_sample_csv("wechat_import_template.csv")

    # Test Weibo
    print("\n[Testing Weibo RSS]")
    weibo = WeiboCollector()

    test_accounts = [
        {"uid": "2123436703", "name": "交通运输部"},
        {"uid": "1921971483", "name": "中国城市轨道交通协会"},
    ]

    posts = weibo.fetch_multiple_users(test_accounts)
    print(f"Found {len(posts)} Weibo posts")

    for post in posts[:3]:
        print(f"  - {post['title'][:50]}...")
        print(f"    Source: {post['source']}")

    print("\n" + "=" * 70)
    print("Data collection complete!")
    print("For production use, consider deploying your own RSSHub instance")
    print("=" * 70)


if __name__ == "__main__":
    main()
