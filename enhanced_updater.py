#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Daily safety data updater with enhanced source configuration
Includes: 54+ Chinese cities, Hong Kong MTR, Weibo, WeChat
"""

import schedule
import time
import logging
import json
import requests
from datetime import datetime

# Import the enhanced scraper
from enhanced_scraper import EnhancedSubwayScraper

# Import data source configuration
from data_sources_config import get_all_data_sources, get_source_statistics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("daily_scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class EnhancedSafetyUpdater:
    def __init__(self, dashboard_api_url="http://localhost:5000/api/update-data"):
        self.scraper = EnhancedSubwayScraper()
        self.dashboard_api_url = dashboard_api_url
        self.data_sources = get_all_data_sources()
        self.stats = get_source_statistics()

    def run_daily_scraping(self):
        """Run the daily scraping routine"""
        logger.info("=" * 70)
        logger.info("Starting daily subway safety data scraping...")
        logger.info(f"Targeting {self.stats['total']} data sources")
        logger.info("=" * 70)

        try:
            # Scrape all sources using enhanced scraper
            scraped_data = self.scraper.scrape_all_sources()

            # Process and format data for dashboard
            dashboard_data = self.process_scraped_data(scraped_data)

            # Save processed data
            self.save_processed_data(dashboard_data)

            # Update dashboard (if API is available)
            self.update_dashboard(dashboard_data)

            logger.info("=" * 70)
            logger.info("Daily scraping completed successfully")
            logger.info(
                f"Total updates collected: {len(dashboard_data['global_metrics']['recent_updates'])}"
            )
            logger.info("=" * 70)

        except Exception as e:
            logger.error(f"Error during daily scraping: {str(e)}")

    def process_scraped_data(self, scraped_data):
        """Process scraped data into dashboard format"""
        # Extract and organize safety updates by region
        chinese_updates = []
        hk_macau_updates = []
        government_updates = []
        international_updates = []

        for city_data in scraped_data["sources"].get("chinese_cities", []):
            if city_data.get("status") == "success":
                chinese_updates.extend(city_data.get("updates", []))

        for metro_data in scraped_data["sources"].get("hk_macau", []):
            if metro_data.get("status") == "success":
                hk_macau_updates.extend(metro_data.get("updates", []))

        for source_data in scraped_data["sources"].get("government", []):
            if source_data.get("status") == "success":
                government_updates.extend(source_data.get("updates", []))

        for source_data in scraped_data["sources"].get("international", []):
            if source_data.get("status") == "success":
                international_updates.extend(source_data.get("updates", []))

        # Calculate regional safety metrics based on scraped data
        regional_data = self.calculate_regional_metrics(scraped_data)

        # Format recent updates for dashboard
        recent_updates = self.format_updates(scraped_data.get("safety_updates", []))

        processed_data = {
            "global_metrics": {
                "total_incidents": len(
                    [
                        u
                        for u in scraped_data.get("safety_updates", [])
                        if "事故" in u.get("title", "")
                        or "accident" in u.get("title", "").lower()
                    ]
                ),
                "recent_updates": recent_updates[:20],  # Limit to 20 most recent
                "data_quality": scraped_data["statistics"].get("successful", 0)
                / max(1, scraped_data["statistics"].get("total_scraped", 1))
                * 100,
            },
            "regional_data": regional_data,
            "data_sources": self.format_data_sources(scraped_data.get("sources", {})),
            "statistics": {
                "total_cities_scraped": scraped_data["statistics"].get(
                    "total_scraped", 0
                ),
                "successful_scrapes": scraped_data["statistics"].get("successful", 0),
                "failed_scrapes": scraped_data["statistics"].get("failed", 0),
                "total_weibo_accounts": self.stats["weibo_accounts"],
                "total_wechat_accounts": self.stats["wechat_accounts"],
            },
            "last_updated": datetime.now().isoformat(),
        }

        return processed_data

    def calculate_regional_metrics(self, scraped_data):
        """Calculate regional safety metrics based on scraped data"""
        # Count safety updates by region
        chinese_count = len(scraped_data["sources"].get("chinese_cities", []))
        hk_count = len(scraped_data["sources"].get("hk_macau", []))

        regional_data = {
            "china": {
                "incidents": 0,
                "safety_score": 95,
                "last_update": datetime.now().isoformat(),
                "cities_scraped": chinese_count,
                "total_cities": self.stats["total_chinese_cities"],
            },
            "hk_macau": {
                "incidents": 0,
                "safety_score": 98,
                "last_update": datetime.now().isoformat(),
                "cities_scraped": hk_count,
                "total_cities": self.stats["hk_macau"],
            },
            "japan": {
                "incidents": 0,
                "safety_score": 98,
                "last_update": datetime.now().isoformat(),
            },
            "europe": {
                "incidents": 0,
                "safety_score": 96,
                "last_update": datetime.now().isoformat(),
            },
            "america": {
                "incidents": 0,
                "safety_score": 92,
                "last_update": datetime.now().isoformat(),
            },
        }

        # Analyze updates to determine incident counts
        all_updates = scraped_data.get("safety_updates", [])

        for update in all_updates:
            title = update.get("title", "").lower()
            source = update.get("source", "")

            # Check for incident keywords
            if any(kw in title for kw in ["事故", "accident", "injury", "伤亡"]):
                if any(city in source for city in ["北京", "上海", "广州", "深圳"]):
                    regional_data["china"]["incidents"] += 1
                elif "香港" in source or "港铁" in source or "MTR" in source:
                    regional_data["hk_macau"]["incidents"] += 1

        return regional_data

    def format_updates(self, updates):
        """Format updates for dashboard display"""
        formatted_updates = []

        for update in updates[:30]:  # Limit to top 30 updates
            formatted_updates.append(
                {
                    "content": update.get("title", ""),
                    "time": update.get("date", datetime.now().strftime("%Y-%m-%d")),
                    "source": update.get("source", "Unknown"),
                    "url": update.get("url", ""),
                }
            )

        return formatted_updates

    def format_data_sources(self, sources):
        """Format data sources for dashboard"""
        formatted_sources = []

        # Add Chinese cities
        for city_data in sources.get("chinese_cities", []):
            formatted_sources.append(
                {
                    "name": city_data.get("name", "Unknown"),
                    "city": city_data.get("city", ""),
                    "url": city_data.get("url", ""),
                    "status": city_data.get("status", "unknown"),
                    "type": "metro_city",
                }
            )

        # Add Hong Kong/Macau
        for metro_data in sources.get("hk_macau", []):
            formatted_sources.append(
                {
                    "name": metro_data.get("name", "Unknown"),
                    "city": metro_data.get("city", ""),
                    "url": metro_data.get("url", ""),
                    "status": metro_data.get("status", "unknown"),
                    "type": "hk_macau",
                }
            )

        # Add government sources
        for source_data in sources.get("government", []):
            formatted_sources.append(
                {
                    "name": source_data.get("name", "Unknown"),
                    "url": source_data.get("url", ""),
                    "status": source_data.get("status", "unknown"),
                    "type": "government",
                }
            )

        # Add international sources
        for source_data in sources.get("international", []):
            formatted_sources.append(
                {
                    "name": source_data.get("name", "Unknown"),
                    "url": source_data.get("url", ""),
                    "status": source_data.get("status", "unknown"),
                    "type": "international",
                }
            )

        return formatted_sources

    def save_processed_data(self, data):
        """Save processed data to file"""
        try:
            filename = f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Processed data saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            return None

    def update_dashboard(self, data):
        """Send processed data to dashboard API"""
        try:
            response = requests.post(
                self.dashboard_api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code == 200:
                logger.info("Dashboard updated successfully")
            else:
                logger.warning(f"Dashboard API returned: {response.status_code}")

        except requests.exceptions.ConnectionError:
            logger.warning("Dashboard API not available (server not running)")
        except Exception as e:
            logger.error(f"Error updating dashboard: {str(e)}")

    def schedule_daily_updates(self):
        """Schedule daily updates at 8:00 AM"""
        schedule.every().day.at("08:00").do(self.run_daily_scraping)

        logger.info("Daily updates scheduled for 8:00 AM")
        logger.info(f"Total data sources configured: {self.stats['total']}")
        logger.info(f"  - Chinese cities: {self.stats['total_chinese_cities']}")
        logger.info(f"  - Hong Kong/Macau: {self.stats['hk_macau']}")
        logger.info(f"  - Government: {self.stats['government']}")
        logger.info(f"  - International: {self.stats['international']}")
        logger.info(f"  - Weibo accounts: {self.stats['weibo_accounts']}")
        logger.info(f"  - WeChat accounts: {self.stats['wechat_accounts']}")

        while True:
            schedule.run_pending()
            time.sleep(60)

    def run_once(self):
        """Run the update process once (for testing)"""
        logger.info("Running one-time update...")
        self.run_daily_scraping()


def main():
    """Main execution"""
    updater = EnhancedSafetyUpdater()

    # Print source statistics
    stats = get_source_statistics()
    print("=" * 70)
    print("Enhanced Safety Data Updater")
    print("=" * 70)
    print(f"Data Source Configuration:")
    print(f"  Chinese Metro Cities: {stats['total_chinese_cities']}")
    print(f"  Hong Kong/Macau:      {stats['hk_macau']}")
    print(f"  Government Sources:   {stats['government']}")
    print(f"  International:         {stats['international']}")
    print(f"  Weibo Accounts:        {stats['weibo_accounts']}")
    print(f"  WeChat Accounts:       {stats['wechat_accounts']}")
    print(f"  TOTAL:                 {stats['total']}")
    print("=" * 70)

    # Run once for testing
    updater.run_once()

    # Uncomment to start scheduled updates:
    # updater.schedule_daily_updates()


if __name__ == "__main__":
    main()
