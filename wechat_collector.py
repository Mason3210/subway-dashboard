#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WeChat Article Collection Module
Multiple methods to collect WeChat Official Account articles
"""

import requests
import json
import logging
import re
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Method 1: Sogou WeChat Search (搜狗微信搜索)
# ============================================================================


class SogouWeChatCollector:
    """
    Collect WeChat articles via Sogou WeChat Search
    Free, no authentication required, but limited results
    """

    def __init__(self):
        self.base_url = "https://weixin.sogou.com/weixin"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )

    def search_articles(self, keyword, limit=10):
        """
        Search WeChat articles by keyword via Sogou

        Args:
            keyword: Search keyword (e.g., "北京地铁 安全")
            limit: Maximum number of results
        """
        articles = []

        try:
            # Sogou WeChat search URL
            encoded_keyword = quote_plus(keyword)
            url = f"{self.base_url}?type=2&query={encoded_keyword}&ie=utf8"

            logger.info(f"Searching Sogou WeChat: {keyword}")

            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Parse search results
            result_items = soup.select("div.news-box li.news-list-item")

            for item in result_items[:limit]:
                try:
                    # Extract title
                    title_elem = item.select_one("h3 a")
                    title = title_elem.get_text().strip() if title_elem else ""

                    # Extract URL
                    url = title_elem.get("href", "") if title_elem else ""

                    # Extract source/time
                    source_elem = item.select_one("div.news-info a")
                    source = source_elem.get_text().strip() if source_elem else ""

                    # Extract description
                    desc_elem = item.select_one("p.news-desc")
                    description = desc_elem.get_text().strip() if desc_elem else ""

                    # Extract date
                    date_elem = item.select_one("span.txt")
                    date = date_elem.get_text().strip() if date_elem else ""

                    if title and url:
                        articles.append(
                            {
                                "title": title,
                                "url": url,
                                "source": source,
                                "description": description,
                                "date": date,
                                "keyword": keyword,
                                "collection_method": "sogou",
                            }
                        )

                except Exception as e:
                    logger.warning(f"Error parsing article: {str(e)}")
                    continue

        except requests.exceptions.Timeout:
            logger.error("Sogou search timeout")
        except Exception as e:
            logger.error(f"Sogou search error: {str(e)}")

        return articles

    def search_multiple_keywords(self, keywords):
        """Search multiple keywords and aggregate results"""
        all_articles = []

        for keyword in keywords:
            articles = self.search_articles(keyword)
            all_articles.extend(articles)
            time.sleep(random.uniform(1, 3))  # Be respectful

        return all_articles


# ============================================================================
# Method 2: WeChat Article Page Crawler
# ============================================================================


class WeChatArticleCollector:
    """
    Collect individual WeChat articles from known URLs
    Requires: WeChat article URLs (can be obtained from Sogou search)
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )

    def fetch_article(self, url):
        """
        Fetch a single WeChat article

        Note: WeChat articles require valid cookies to access
        This is a simplified version
        """
        article_data = {
            "url": url,
            "status": "unknown",
            "title": "",
            "content": "",
            "author": "",
            "publish_date": "",
            "read_count": 0,
            "like_count": 0,
        }

        try:
            response = self.session.get(url, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # Try to extract title
                title_elem = soup.select_one("#activity-name")
                if title_elem:
                    article_data["title"] = title_elem.get_text().strip()

                # Try to extract content
                content_elem = soup.select_one("#js_content")
                if content_elem:
                    article_data["content"] = content_elem.get_text()[
                        :500
                    ]  # First 500 chars

                # Try to extract author
                author_elem = soup.select_one("#js_author_name")
                if author_elem:
                    article_data["author"] = author_elem.get_text().strip()

                article_data["status"] = "success"

        except Exception as e:
            article_data["status"] = "error"
            article_data["error"] = str(e)

        return article_data

    def fetch_with_cookie(self, url, cookie):
        """
        Fetch article with WeChat cookie
        More reliable but requires manual cookie setup
        """
        self.session.headers.update({"Cookie": cookie})
        return self.fetch_article(url)


# ============================================================================
# Method 3: Search Engine Collection (Bing/Google)
# ============================================================================


class SearchEngineCollector:
    """
    Collect WeChat articles via search engines
    Use Bing to find WeChat articles
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
        )

    def search_bing(self, keyword, site="weixin.qq.com", limit=10):
        """
        Search Bing for WeChat articles

        Args:
            keyword: Search keyword
            site: Restrict to specific site (default: weixin.qq.com)
            limit: Maximum results
        """
        articles = []

        try:
            # Use DuckDuckGo or Bing API
            query = f"{keyword} site:{site}"
            encoded_query = quote_plus(query)

            # DuckDuckGo (free, no API key needed)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")

            for result in soup.select("a.result__a")[:limit]:
                title = result.get_text().strip()
                link = result.get("href", "")

                # Filter for WeChat article links
                if "mp.weixin.qq.com" in link or "weixin.qq.com" in link:
                    articles.append(
                        {
                            "title": title,
                            "url": link,
                            "keyword": keyword,
                            "collection_method": "search_engine",
                        }
                    )

        except Exception as e:
            logger.error(f"Search error: {str(e)}")

        return articles


# ============================================================================
# Method 4: WeChat PC Client Hook (Advanced)
# ============================================================================


class WeChatPluginCollector:
    """
    Method to capture articles from WeChat PC Client

    This requires:
    1. WeChat PC client running
    2. Hook library (e.g., Frida, pywinhook)
    3. Capture the message when article is pushed

    This is a reference implementation - requires additional setup
    """

    @staticmethod
    def get_reference_info():
        """
        Get reference information for WeChat plugin method

        See: https://github.com/yeximm/Access_wechat_article
        """
        return {
            "method": "WeChat PC Client Hook",
            "description": "Hook WeChat Windows client to capture article links in real-time",
            "requirements": [
                "WeChat for Windows (not WeChat for Mac)",
                "Python with pywinhook or Frida",
                "Technical knowledge for setup",
            ],
            "reference": "https://github.com/yeximm/Access_wechat_article",
            "note": "This is the most reliable method but requires complex setup",
        }


# ============================================================================
# Unified WeChat Collector
# ============================================================================


class UnifiedWeChatCollector:
    """
    Unified WeChat collector using multiple methods
    Priority: Sogou > Search Engine > Manual
    """

    def __init__(self):
        self.sogou = SogouWeChatCollector()
        self.search_engine = SearchEngineCollector()
        self.article = WeChatArticleCollector()

    def collect_by_keywords(self, keywords, method="all"):
        """
        Collect articles by keywords using available methods

        Args:
            keywords: List of keywords to search
            method: 'sogou', 'search', or 'all'
        """
        all_articles = []

        safety_keywords = (
            keywords
            if keywords
            else [
                "地铁 安全",
                "轨道交通 事故",
                "地铁 故障",
                "地铁 延误",
                "交通局 安全",
                "应急管理 预警",
            ]
        )

        if method in ["sogou", "all"]:
            logger.info("Collecting via Sogou WeChat Search...")
            sogou_articles = self.sogou.search_multiple_keywords(safety_keywords)
            all_articles.extend(sogou_articles)
            logger.info(f"Found {len(sogou_articles)} articles from Sogou")

        if method in ["search", "all"]:
            logger.info("Collecting via Search Engine...")
            for keyword in safety_keywords:
                search_articles = self.search_engine.search_bing(keyword)
                all_articles.extend(search_articles)
                time.sleep(2)

        # Remove duplicates
        seen = set()
        unique_articles = []
        for article in all_articles:
            if article["url"] not in seen:
                seen.add(article["url"])
                unique_articles.append(article)

        logger.info(f"Total unique articles: {len(unique_articles)}")
        return unique_articles

    def collect_by_accounts(self, account_names):
        """
        Collect articles from specific WeChat accounts

        Args:
            account_names: List of account names to search
        """
        keywords = [f"{name} 安全" for name in account_names]
        return self.collect_by_keywords(keywords)


# ============================================================================
# Main Function
# ============================================================================


def main():
    print("=" * 60)
    print("WeChat Article Collection Module")
    print("=" * 60)

    # Test with sample keywords
    collector = UnifiedWeChatCollector()

    test_keywords = ["北京地铁 安全", "上海地铁 运营", "交通部 预警", "应急管理 安全"]

    print("\nTesting collection with sample keywords...")
    print("-" * 40)

    # This will actually try to fetch (may fail due to anti-crawling)
    # Uncomment to test:
    # articles = collector.collect_by_keywords(test_keywords)
    # for a in articles[:5]:
    #     print(f"- {a['title'][:50]}...")

    print("\nAvailable Methods:")
    print("1. Sogou WeChat Search - Free, limited results")
    print("2. Search Engine - Uses DuckDuckGo")
    print("3. WeChat Article API - Requires cookies")
    print("4. WeChat Plugin - Requires PC client hook")

    print("\n" + "=" * 60)
    print("To run actual collection:")
    print(
        'python -c "from social_media_collector import *; '
        "c = UnifiedWeChatCollector(); "
        "c.collect_by_keywords(['地铁 安全'])\""
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
