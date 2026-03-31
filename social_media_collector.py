#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Social Media Data Collection Module
WeChat and Weibo account configuration and collection strategies

Technical Limitations:
- WeChat: No public API available, requires third-party services or manual data import
- Weibo: RSSHub can generate RSS feeds for public accounts
"""

import requests
import json
import logging
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# WeChat Official Accounts Configuration
# ============================================================================

WECHAT_ACCOUNTS = {
    # Metro Companies (50+ cities)
    "metro": [
        {"name": "北京地铁", "id": "bjsubway", "city": "北京"},
        {"name": "上海地铁", "id": "shmetro", "city": "上海"},
        {"name": "广州地铁", "id": "gzmtr105", "city": "广州"},
        {"name": "深圳地铁", "id": "shenzhenmetro", "city": "深圳"},
        {"name": "成都地铁", "id": "chengdumetro", "city": "成都"},
        {"name": "杭州地铁", "id": "hangzhoumetro", "city": "杭州"},
        {"name": "武汉地铁", "id": "wuhanmetro", "city": "武汉"},
        {"name": "西安地铁", "id": "xianmetro", "city": "西安"},
        {"name": "重庆轨道", "id": "cqmetro", "city": "重庆"},
        {"name": "天津地铁", "id": "tjmetro", "city": "天津"},
        {"name": "南京地铁", "id": "njdtglzx", "city": "南京"},
        {"name": "苏州轨道交通", "id": "sz-mtr", "city": "苏州"},
        {"name": "郑州地铁", "id": "zzmetro", "city": "郑州"},
        {"name": "长沙地铁", "id": "hncsmtr", "city": "长沙"},
        {"name": "沈阳地铁", "id": "symtc", "city": "沈阳"},
        {"name": "宁波轨道交通", "id": "nbgdjt", "city": "宁波"},
        {"name": "青岛地铁", "id": "qdmtr", "city": "青岛"},
        {"name": "大连地铁", "id": "dalianmetro", "city": "大连"},
        {"name": "东莞轨道交通", "id": "dggdjt", "city": "东莞"},
        {"name": "无锡地铁", "id": "wuximetro", "city": "无锡"},
        {"name": "佛山地铁", "id": "foshanmetro", "city": "佛山"},
        {"name": "南宁轨道交通", "id": "nnzdtz", "city": "南宁"},
    ],
    # National Government
    "national": [
        {"name": "交通运输部", "id": "MOT-gov", "type": "transportation"},
        {"name": "中国交通报", "id": "zgjtbwx", "type": "media"},
        {"name": "中国城市轨道交通协会", "id": "camet123", "type": "association"},
        {"name": "应急管理部", "id": "yjglb", "type": "emergency"},
        {"name": "国家铁路局", "id": "nragov", "type": "rail"},
    ],
    # Provincial Transportation
    "provincial_transportation": [
        {"name": "广东交通", "id": "gdjtweb", "province": "广东"},
        {"name": "江苏交通", "id": "jsjtgl", "province": "江苏"},
        {"name": "浙江交通", "id": "zjtv-org", "province": "浙江"},
        {"name": "山东交通", "id": "sd-jtys", "province": "山东"},
        {"name": "河南交通", "id": "hnjtys", "province": "河南"},
        {"name": "四川交通", "id": "scjt2014", "province": "四川"},
        {"name": "湖北交通", "id": "hbjt2022", "province": "湖北"},
        {"name": "湖南交通", "id": "hnjtgl", "province": "湖南"},
        {"name": "安徽交通", "id": "ahjtgl", "province": "安徽"},
        {"name": "福建交通", "id": "fjjtgl", "province": "福建"},
    ],
    # Provincial Emergency Management
    "provincial_emergency": [
        {"name": "广东应急管理", "id": "gdyjgl", "province": "广东"},
        {"name": "江苏应急管理", "id": "jssyjgl", "province": "江苏"},
        {"name": "浙江应急管理", "id": "zjyjjt", "province": "浙江"},
        {"name": "山东应急管理", "id": "sdyjgl", "province": "山东"},
        {"name": "河南应急管理", "id": "henanyjgl", "province": "河南"},
        {"name": "四川应急管理", "id": "scyjgl", "province": "四川"},
        {"name": "湖北应急管理", "id": "hbyjgl", "province": "湖北"},
        {"name": "湖南应急管理", "id": "hnsyjgl", "province": "湖南"},
    ],
    # City Transportation Bureaus
    "city_transportation": [
        {"name": "北京交通", "id": "bj-jtw", "city": "北京"},
        {"name": "上海交通", "id": "shanghai-jiaotong", "city": "上海"},
        {"name": "广州交通", "id": "gzjiaotong", "city": "广州"},
        {"name": "深圳交通", "id": "szjt", "city": "深圳"},
        {"name": "成都交通", "id": "cdjt", "city": "成都"},
    ],
    # City Emergency Management Bureaus
    "city_emergency": [
        {"name": "北京应急", "id": "bjyjj", "city": "北京"},
        {"name": "上海应急", "id": "shanghai-yingji", "city": "上海"},
        {"name": "广州应急", "id": "gzyjj", "city": "广州"},
        {"name": "深圳应急", "id": "szyjj", "city": "深圳"},
        {"name": "成都应急", "id": "cdyjj", "city": "成都"},
    ],
}


# ============================================================================
# Weibo Accounts Configuration
# ============================================================================

WEIBO_ACCOUNTS = {
    # Metro Companies
    "metro": [
        {"name": "北京地铁", "uid": "1921971483", "city": "北京"},
        {"name": "上海地铁", "uid": "1780024675", "city": "上海"},
        {"name": "广州地铁", "uid": "1682624913", "city": "广州"},
        {"name": "深圳地铁", "uid": "1665243115", "city": "深圳"},
        {"name": "成都地铁", "uid": "1823881805", "city": "成都"},
        {"name": "杭州地铁", "uid": "1739347920", "city": "杭州"},
        {"name": "武汉地铁", "uid": "1853384914", "city": "武汉"},
        {"name": "西安地铁", "uid": "1853384721", "city": "西安"},
        {"name": "重庆轨道", "uid": "1848646862", "city": "重庆"},
        {"name": "天津地铁", "uid": "1825056707", "city": "天津"},
        {"name": "南京地铁", "uid": "2029627982", "city": "南京"},
        {"name": "苏州轨道交通", "uid": "2649271183", "city": "苏州"},
        {"name": "郑州地铁", "uid": "2991504987", "city": "郑州"},
        {"name": "长沙地铁", "uid": "2068719825", "city": "长沙"},
        {"name": "沈阳地铁", "uid": "2067085047", "city": "沈阳"},
        {"name": "宁波轨道交通", "uid": "2997569825", "city": "宁波"},
        {"name": "青岛地铁", "uid": "2990419823", "city": "青岛"},
        {"name": "大连地铁", "uid": "2029406925", "city": "大连"},
        {"name": "东莞轨道交通", "uid": "", "city": "东莞"},
        {"name": "无锡地铁", "uid": "2986931825", "city": "无锡"},
        {"name": "佛山地铁", "uid": "", "city": "佛山"},
        {"name": "南宁轨道交通", "uid": "", "city": "南宁"},
    ],
    # National Government
    "national": [
        {"name": "交通运输部", "uid": "2123436703", "type": "transportation"},
        {"name": "中国城市轨道交通协会", "uid": "1921971483", "type": "association"},
        {"name": "应急管理部", "uid": "6286498603", "type": "emergency"},
        {"name": "中国消防", "uid": "2189823192", "type": "emergency"},
        {"name": "国家铁路局", "uid": "", "type": "rail"},
    ],
    # Provincial Transportation
    "provincial_transportation": [
        {"name": "广东交通", "uid": "", "province": "广东"},
        {"name": "江苏交通", "uid": "", "province": "江苏"},
        {"name": "浙江交通", "uid": "", "province": "浙江"},
    ],
    # Provincial Emergency
    "provincial_emergency": [
        {"name": "山东应急管理", "uid": "", "province": "山东"},
        {"name": "广东应急管理", "uid": "", "province": "广东"},
    ],
}


# ============================================================================
# WeChat Data Collector (Mock - requires third-party service)
# ============================================================================


class WeChatCollector:
    """
    WeChat data collector
    NOTE: WeChat Official Account APIs are not publicly available.
    This module provides structure for manual data import or third-party integration.
    """

    def __init__(self):
        self.accounts = WECHAT_ACCOUNTS
        self.data = []

    def collect_all(self):
        """Collect data from all WeChat accounts"""
        logger.info("WeChat collection - NOTE: No public API available")
        logger.info("Options:")
        logger.info("  1. Use third-party services (NewRank, GsData)")
        logger.info("  2. Manual CSV/Excel import")
        logger.info("  3. Use Sogou WeChat search (limited)")

        # This is a placeholder - real implementation requires:
        # - Third-party API keys (新榜, 清博, 西瓜数据)
        # - Or manual data import

        return {
            "status": "requires_manual_import",
            "accounts_count": self.get_total_accounts(),
            "instructions": "Please import WeChat data via CSV/Excel format",
        }

    def get_total_accounts(self):
        """Get total number of configured accounts"""
        total = 0
        for category in self.accounts.values():
            total += len(category)
        return total

    def export_account_list(self, filename="wechat_accounts.csv"):
        """Export account list for manual data collection"""
        import csv

        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["名称", "ID", "类型/城市", "类别"])

            for category, accounts in self.accounts.items():
                for account in accounts:
                    writer.writerow(
                        [
                            account.get("name", ""),
                            account.get("id", ""),
                            account.get("city", account.get("province", "")),
                            category,
                        ]
                    )

        logger.info(f"WeChat account list exported to {filename}")
        return filename


# ============================================================================
# Weibo Data Collector
# ============================================================================


class WeiboCollector:
    """
    Weibo data collector using RSSHub
    RSSHub provides free RSS feeds for many Chinese websites including Weibo

    Alternative: Use weibo-search RSS feed from RSSHub
    """

    def __init__(self, rsshub_urls=None):
        self.accounts = WEIBO_ACCOUNTS
        self.rsshub_urls = rsshub_urls or [
            "https://rsshub.app",
            "https://api.rsshub.app",
        ]
        self.data = []

    def collect_all(self):
        """Collect data from all Weibo accounts via RSS"""
        logger.info("Collecting Weibo data via RSS...")

        all_posts = []

        for category, accounts in self.accounts.items():
            for account in accounts:
                if account.get("uid") and account.get("uid") != "":
                    posts = self.fetch_weibo_rss(account)
                    all_posts.extend(posts)
                    time.sleep(1)  # Be respectful

        return {
            "status": "success" if all_posts else "partial",
            "posts_count": len(all_posts),
            "posts": all_posts[:50],
        }

    def fetch_weibo_rss(self, account):
        """Fetch Weibo posts via RSSHub with fallback URLs"""
        posts = []

        for rsshub_url in self.rsshub_urls:
            try:
                uid = account.get("uid")
                url = f"{rsshub_url}/weibo/user/{uid}"

                response = requests.get(
                    url,
                    timeout=30,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                )

                if response.status_code == 200:
                    from xml.etree import ElementTree

                    root = ElementTree.fromstring(response.content)

                    for item in root.findall(".//item"):
                        title = (
                            item.find("title").text
                            if item.find("title") is not None
                            else ""
                        )
                        link = (
                            item.find("link").text
                            if item.find("link") is not None
                            else ""
                        )
                        pubDate = (
                            item.find("pubDate").text
                            if item.find("pubDate") is not None
                            else ""
                        )
                        description = (
                            item.find("description").text
                            if item.find("description") is not None
                            else ""
                        )

                        if self.is_safety_related(title + " " + description):
                            posts.append(
                                {
                                    "title": title,
                                    "link": link,
                                    "date": pubDate,
                                    "source": account.get("name"),
                                    "account_type": account.get(
                                        "city", account.get("type", "")
                                    ),
                                }
                            )
                    break

            except Exception as e:
                logger.warning(f"Error fetching Weibo RSS from {rsshub_url}: {str(e)}")
                continue

        return posts

    def is_safety_related(self, text):
        """Check if text contains safety-related keywords"""
        keywords = [
            "安全",
            "事故",
            "故障",
            "延误",
            "中断",
            "紧急",
            "救援",
            "injury",
            "accident",
            "emergency",
            "safety",
            "incident",
            "停运",
            "晚点",
            "运营调整",
            "客流管控",
            "设备故障",
            "信号故障",
            "道床故障",
            "车门",
            "站台门",
            "列车",
            "轨道",
            "供电",
            "防汛",
            "暴风雨",
            "大客流",
            "疏散",
            "应急",
            "演练",
            "检查",
            "整改",
            "隐患",
        ]
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in keywords)

    def collect_with_cookie(self, cookie=None):
        """
        Alternative: Use Weibo API with cookie
        Requires: Weibo login cookie (may expire, use at your own risk)
        """
        if not cookie:
            logger.warning("Weibo API requires valid cookie. Using RSS fallback.")
            return self.collect_all()

        # This would be a more complete implementation
        # but requires maintaining valid cookies
        pass

    def get_total_accounts(self):
        """Get total number of configured accounts"""
        total = 0
        for category in self.accounts.values():
            total += len(
                [a for a in category if a.get("uid") and a.get("uid") != "待补充"]
            )
        return total

    def export_account_list(self, filename="weibo_accounts.csv"):
        """Export account list for reference"""
        import csv

        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["名称", "UID", "类型/城市", "类别"])

            for category, accounts in self.accounts.items():
                for account in accounts:
                    writer.writerow(
                        [
                            account.get("name", ""),
                            account.get("uid", ""),
                            account.get("city", account.get("province", "")),
                            category,
                        ]
                    )

        logger.info(f"Weibo account list exported to {filename}")
        return filename


# ============================================================================
# Manual Data Import Utilities
# ============================================================================


def import_csv_data(filename, platform="wechat"):
    """
    Import manual data from CSV/Excel

    CSV Format (WeChat):
    日期,标题,链接,公众号名称,阅读量,类型

    CSV Format (Weibo):
    日期,内容,链接,微博账号,点赞数,类型
    """
    import csv

    data = []
    try:
        with open(filename, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        logger.info(f"Imported {len(data)} records from {filename}")
        return data

    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return []
    except Exception as e:
        logger.error(f"Error importing data: {str(e)}")
        return []


def export_sample_csv(platform="wechat", filename="sample_import.csv"):
    """Export sample CSV template for manual data import"""
    import csv

    if platform == "wechat":
        headers = ["日期", "标题", "链接", "公众号名称", "城市", "安全类型", "摘要"]
    else:
        headers = ["日期", "内容", "链接", "微博账号", "城市", "安全类型", "点赞数"]

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        # Add sample row
        writer.writerow(
            [
                "2024-01-01",
                "示例标题",
                "https://example.com",
                "地铁公司",
                "北京",
                "安全演练",
                "摘要内容",
            ]
        )

    logger.info(f"Sample CSV template exported to {filename}")
    return filename


# ============================================================================
# Main Test Function
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Social Media Data Collection Module")
    print("=" * 60)

    # Test WeChat
    print("\n[WeChat Collector]")
    wechat = WeChatCollector()
    print(f"Total WeChat accounts configured: {wechat.get_total_accounts()}")
    wechat.export_account_list("wechat_accounts.csv")

    # Test Weibo
    print("\n[Weibo Collector]")
    weibo = WeiboCollector()
    print(f"Total Weibo accounts (with UID): {weibo.get_total_accounts()}")
    weibo.export_account_list("weibo_accounts.csv")

    # Export sample CSV
    print("\n[Manual Import Templates]")
    export_sample_csv("wechat", "wechat_import_sample.csv")
    export_sample_csv("weibo", "weibo_import_sample.csv")

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Edit wechat_accounts.csv - add your WeChat IDs")
    print("2. Edit weibo_accounts.csv - add your Weibo UIDs")
    print("3. For WeChat: Use third-party service or manual import")
    print("4. For Weibo: Try RSSHub or maintain valid cookies")
    print("=" * 60)
