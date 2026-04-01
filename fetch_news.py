#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
News Fetcher for GitHub Pages Deployment
========================================

This script fetches the latest news and saves it to a JSON file.
It is designed to be run by:
1. GitHub Actions (scheduled daily)
2. Local development (manual run)
3. Any CI/CD pipeline

The frontend index.html loads data from news_data.json
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from comprehensive_news_aggregator import MultiSourceScraper
from data_sources_config import SOCIAL_MEDIA_SOURCES

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_and_save_news():
    """
    Main function: Fetch news and save to JSON file
    Returns True if successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info("Fetching latest subway safety news...")
    logger.info("=" * 60)

    try:
        # Initialize scraper
        scraper = MultiSourceScraper()

        # Get Weibo accounts from config
        weibo_accounts = []
        for account in SOCIAL_MEDIA_SOURCES.get("weibo", []):
            if account.get("uid") and account["uid"] not in ["", "待补充"]:
                weibo_accounts.append(account)

        logger.info(f"Using {len(weibo_accounts)} Weibo accounts")

        # Fetch all news
        news_items = scraper.collect_all(weibo_accounts=weibo_accounts)

        if not news_items:
            logger.warning("No news items collected!")
            return False

        # Convert to frontend format
        events = []
        for item in news_items:
            events.append(
                {
                    "id": abs(hash(item.content_hash)) % 1000000,
                    "time": item.publish_date[:10]
                    if item.publish_date
                    else datetime.now().strftime("%Y-%m-%d"),
                    "title": item.title,
                    "source": item.source,
                    "category": item.category,
                    "url": item.url if item.url else "#",
                    "isNew": False,
                    "summary": item.summary
                    or f"来源: {item.source}。关键词: {', '.join(item.keywords[:5])}",
                    "verified": item.verified,
                }
            )

        # Sort by time (newest first)
        events.sort(key=lambda x: x["time"], reverse=True)

        # Assign isNew flag to top 10
        for i, event in enumerate(events[:10]):
            event["isNew"] = True

        # Save to JSON
        output_data = {
            "updated_at": datetime.now().isoformat(),
            "total_events": len(events),
            "events": events,
            "statistics": {
                "by_category": {
                    "safety": len([e for e in events if e["category"] == "safety"]),
                    "law": len([e for e in events if e["category"] == "law"]),
                    "news": len([e for e in events if e["category"] == "news"]),
                    "technology": len(
                        [e for e in events if e["category"] == "technology"]
                    ),
                    "operation": len(
                        [e for e in events if e["category"] == "operation"]
                    ),
                },
                "sources_tried": scraper.stats.get("sources_tried", 0),
                "successful_sources": scraper.stats.get("successful_sources", 0),
            },
        }

        # Save to news_data.json (used by frontend)
        output_file = Path(__file__).parent / "news_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Successfully saved {len(events)} events to {output_file}")
        logger.info(f"Category breakdown: {output_data['statistics']['by_category']}")

        # Also save to data directory for backup
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(exist_ok=True)

        backup_file = (
            data_dir / f"news_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Backup saved to {backup_file}")

        return True

    except Exception as e:
        logger.error(f"Failed to fetch news: {e}")
        import traceback

        traceback.print_exc()
        return False


def update_frontend_data():
    """
    Update the index.html with the latest data
    This is used for static site generation
    """
    try:
        news_file = Path(__file__).parent / "news_data.json"

        if not news_file.exists():
            logger.warning("news_data.json not found, skipping frontend update")
            return False

        with open(news_file, "r", encoding="utf-8") as f:
            news_data = json.load(f)

        logger.info(f"Frontend data ready with {news_data['total_events']} events")
        return True

    except Exception as e:
        logger.error(f"Failed to update frontend data: {e}")
        return False


if __name__ == "__main__":
    success = fetch_and_save_news()

    if success:
        update_frontend_data()
        logger.info("=" * 60)
        logger.info("News fetch completed successfully!")
        logger.info("=" * 60)
        sys.exit(0)
    else:
        logger.error("=" * 60)
        logger.error("News fetch failed!")
        logger.error("=" * 60)
        sys.exit(1)
