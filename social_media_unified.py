#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unified Social Media Data Collector
Combines WeChat and Weibo collection with multiple methods
"""

import requests
import json
import logging
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup

# Import the search-based collectors
from wechat_collector import UnifiedWeChatCollector
from social_media_collector import WeiboCollector, WECHAT_ACCOUNTS, WEIBO_ACCOUNTS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("social_media.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


class SocialMediaDataCollector:
    """
    Unified social media data collector
    - WeChat: Sogou search + Search engine + Manual import
    - Weibo: RSSHub + Manual import
    """

    def __init__(self):
        self.wechat = UnifiedWeChatCollector()
        self.weibo = WeiboCollector()
        self.stats = {"wechat_articles": 0, "weibo_posts": 0, "last_collection": None}

    def collect_all(self, keywords=None):
        """
        Collect all social media data

        Args:
            keywords: List of keywords for WeChat search
        """
        all_data = {
            "collected_at": datetime.now().isoformat(),
            "wechat": [],
            "weibo": [],
            "statistics": {},
        }

        # Collect WeChat via Sogou/Search
        if keywords is None:
            keywords = self._get_default_keywords()

        logger.info("Starting social media collection...")

        # Try WeChat collection
        try:
            logger.info("Collecting WeChat articles...")
            wechat_data = self.wechat.collect_by_keywords(
                keywords[:5]
            )  # Limit to avoid rate limit
            all_data["wechat"] = wechat_data
            self.stats["wechat_articles"] = len(wechat_data)
            logger.info(f"WeChat: Found {len(wechat_data)} articles")
        except Exception as e:
            logger.error(f"WeChat collection error: {str(e)}")
            all_data["wechat"] = []

        time.sleep(2)

        # Try Weibo collection via RSS
        try:
            logger.info("Collecting Weibo posts...")
            weibo_data = self.weibo.collect_all()
            all_data["weibo"] = weibo_data.get("posts", [])
            self.stats["weibo_posts"] = len(all_data["weibo"])
            logger.info(f"Weibo: Found {len(all_data['weibo'])} posts")
        except Exception as e:
            logger.error(f"Weibo collection error: {str(e)}")
            all_data["weibo"] = []

        self.stats["last_collection"] = datetime.now().isoformat()
        all_data["statistics"] = self.stats

        return all_data

    def _get_default_keywords(self):
        """Get default search keywords for safety-related content"""
        return [
            # Metro safety
            "地铁 安全事故",
            "地铁 故障",
            "地铁 延误",
            "轨道交通 预警",
            # Government
            "交通部 安全",
            "应急管理部 预警",
            "省交通厅 安全",
            # City
            "市交通局 安全",
            "应急管理局 预警",
        ]

    def collect_by_accounts(self, account_names):
        """
        Collect data from specific accounts

        Args:
            account_names: List of account names
        """
        return self.wechat.collect_by_accounts(account_names)

    def import_manual_data(self, filename, platform):
        """
        Import manual data from CSV file

        Args:
            filename: CSV file path
            platform: 'wechat' or 'weibo'
        """
        from social_media_collector import import_csv_data

        return import_csv_data(filename, platform)

    def get_account_statistics(self):
        """Get statistics about configured accounts"""
        # Count WeChat accounts
        wechat_total = 0
        for category in WECHAT_ACCOUNTS.values():
            wechat_total += len(category)

        # Count Weibo accounts (with valid UID)
        weibo_total = 0
        for category in WEIBO_ACCOUNTS.values():
            weibo_total += len(
                [a for a in category if a.get("uid") and a.get("uid") != "待补充"]
            )

        return {
            "wechat_accounts": wechat_total,
            "weibo_accounts": weibo_total,
            "weibo_with_uid": len(
                [a for a in WEIBO_ACCOUNTS.get("metro", []) if a.get("uid") != "待补充"]
            ),
        }

    def save_data(self, data, filename=None):
        """Save collected data to JSON file"""
        if filename is None:
            filename = (
                f"social_media_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Social media data saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return None


# ============================================================================
# Export Account Lists
# ============================================================================


def export_all_account_lists():
    """Export all account lists to CSV files for reference"""
    import csv

    # Export WeChat accounts
    wechat_file = "wechat_all_accounts.csv"
    with open(wechat_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["名称", "ID", "城市/省份", "类别"])

        for category, accounts in WECHAT_ACCOUNTS.items():
            for account in accounts:
                writer.writerow(
                    [
                        account.get("name", ""),
                        account.get("id", ""),
                        account.get("city", account.get("province", "")),
                        category,
                    ]
                )
    logger.info(f"WeChat accounts exported to {wechat_file}")

    # Export Weibo accounts
    weibo_file = "weibo_all_accounts.csv"
    with open(weibo_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["名称", "UID", "城市/省份", "类别"])

        for category, accounts in WEIBO_ACCOUNTS.items():
            for account in accounts:
                writer.writerow(
                    [
                        account.get("name", ""),
                        account.get("uid", ""),
                        account.get("city", account.get("province", "")),
                        category,
                    ]
                )
    logger.info(f"Weibo accounts exported to {weibo_file}")

    return wechat_file, weibo_file


# ============================================================================
# Main
# ============================================================================


def main():
    print("=" * 60)
    print("Unified Social Media Data Collector")
    print("=" * 60)

    # Show account statistics
    collector = SocialMediaDataCollector()
    stats = collector.get_account_statistics()

    print(f"\nConfigured Accounts:")
    print(f"  WeChat Accounts: {stats['wechat_accounts']}")
    print(f"  Weibo Accounts: {stats['weibo_accounts']}")
    print(f"  Weibo (with UID): {stats['weibo_with_uid']}")

    print("\n" + "-" * 60)
    print("Running test collection...")
    print("-" * 60)

    # Run collection (with limited keywords for speed)
    test_keywords = ["地铁 安全", "交通 安全"]
    data = collector.collect_all(keywords=test_keywords)

    print(f"\nCollection Results:")
    print(f"  WeChat articles: {len(data['wechat'])}")
    print(f"  Weibo posts: {len(data['weibo'])}")

    # Save data
    filename = collector.save_data(data)
    if filename:
        print(f"  Data saved to: {filename}")

    # Export account lists
    export_all_account_lists()
    print("\nAccount lists exported:")
    print("  - wechat_all_accounts.csv")
    print("  - weibo_all_accounts.csv")

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Review wechat_all_accounts.csv - verify account IDs")
    print("2. Review weibo_all_accounts.csv - add missing UIDs")
    print("3. Run collection daily with: python social_media_updater.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
