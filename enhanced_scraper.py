#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced scraper for comprehensive subway safety data collection
Includes: 54+ Chinese cities, Hong Kong MTR, Weibo, WeChat
"""

import requests
import json
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
import random

# Import data source configuration
from data_sources_config import (
    CHINESE_METRO_CITIES,
    HK_MACAU_METRO,
    GOVERNMENT_SOURCES,
    PROVINCIAL_SOURCES,
    CITY_GOVERNMENT_SOURCES,
    MUNICIPALITY_SOURCES,
    INTERNATIONAL_SOURCES,
    SOCIAL_MEDIA_SOURCES,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class EnhancedSubwayScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
        )

        # Safety-related keywords for content filtering
        self.safety_keywords = [
            "安全",
            "事故",
            "事件",
            "故障",
            "延误",
            "中断",
            "救援",
            "紧急",
            "safety",
            "incident",
            "accident",
            "emergency",
            "delay",
            "disruption",
        ]

        # Statistics
        self.stats = {
            "total_scraped": 0,
            "successful": 0,
            "failed": 0,
            "start_time": None,
        }

    def scrape_all_sources(self):
        """Scrape all configured data sources"""
        self.stats["start_time"] = datetime.now()
        all_data = {
            "scraped_at": datetime.now().isoformat(),
            "sources": {
                "chinese_cities": [],
                "hk_macau": [],
                "government": [],
                "provincial_transportation": [],
                "provincial_emergency": [],
                "city_transportation": [],
                "city_emergency": [],
                "municipalities": [],
                "international": [],
                "social_media": [],
            },
            "safety_updates": [],
            "statistics": {},
        }

        # Scrape Chinese metro cities
        logger.info(
            f"Starting to scrape {len(CHINESE_METRO_CITIES)} Chinese metro cities..."
        )
        for city in CHINESE_METRO_CITIES:
            try:
                city_data = self.scrape_metro_city(city)
                all_data["sources"]["chinese_cities"].append(city_data)
                if city_data["status"] == "success":
                    all_data["safety_updates"].extend(city_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {city['name']}: {str(e)}")
                all_data["sources"]["chinese_cities"].append(
                    {"name": city["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(1, 3))  # Random delay to be respectful

        # Scrape Hong Kong/Macau
        logger.info(f"Scraping Hong Kong/Macau metro systems...")
        for metro in HK_MACAU_METRO:
            try:
                metro_data = self.scrape_metro_city(metro)
                all_data["sources"]["hk_macau"].append(metro_data)
                if metro_data["status"] == "success":
                    all_data["safety_updates"].extend(metro_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {metro['name']}: {str(e)}")
                all_data["sources"]["hk_macau"].append(
                    {"name": metro["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(2, 5))

        # Scrape national government sources
        logger.info(f"Scraping national government sources...")
        for source in GOVERNMENT_SOURCES:
            try:
                source_data = self.scrape_website(source)
                all_data["sources"]["government"].append(source_data)
                if source_data["status"] == "success":
                    all_data["safety_updates"].extend(source_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")
                all_data["sources"]["government"].append(
                    {"name": source["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(2, 5))

        # Scrape provincial transportation departments
        logger.info(f"Scraping {len(PROVINCIAL_SOURCES['transportation'])} provincial transportation departments...")
        for source in PROVINCIAL_SOURCES["transportation"]:
            try:
                source_data = self.scrape_website(source)
                all_data["sources"]["provincial_transportation"].append(source_data)
                if source_data["status"] == "success":
                    all_data["safety_updates"].extend(source_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")
                all_data["sources"]["provincial_transportation"].append(
                    {"name": source["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(1, 3))

        # Scrape provincial emergency management departments
        logger.info(f"Scraping {len(PROVINCIAL_SOURCES['emergency_management'])} provincial emergency management departments...")
        for source in PROVINCIAL_SOURCES["emergency_management"]:
            try:
                source_data = self.scrape_website(source)
                all_data["sources"]["provincial_emergency"].append(source_data)
                if source_data["status"] == "success":
                    all_data["safety_updates"].extend(source_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")
                all_data["sources"]["provincial_emergency"].append(
                    {"name": source["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(1, 3))

        # Scrape city transportation bureaus
        logger.info(f"Scraping {len(CITY_GOVERNMENT_SOURCES['transportation_bureaus'])} city transportation bureaus...")
        for source in CITY_GOVERNMENT_SOURCES["transportation_bureaus"]:
            try:
                source_data = self.scrape_website(source)
                all_data["sources"]["city_transportation"].append(source_data)
                if source_data["status"] == "success":
                    all_data["safety_updates"].extend(source_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")
                all_data["sources"]["city_transportation"].append(
                    {"name": source["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(1, 3))

        # Scrape city emergency management bureaus
        logger.info(f"Scraping {len(CITY_GOVERNMENT_SOURCES['emergency_management_bureaus'])} city emergency management bureaus...")
        for source in CITY_GOVERNMENT_SOURCES["emergency_management_bureaus"]:
            try:
                source_data = self.scrape_website(source)
                all_data["sources"]["city_emergency"].append(source_data)
                if source_data["status"] == "success":
                    all_data["safety_updates"].extend(source_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")
                all_data["sources"]["city_emergency"].append(
                    {"name": source["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(1, 3))

        # Scrape municipality sources
        logger.info(f"Scraping municipality sources...")
        for city_name, sources in MUNICIPALITY_SOURCES.items():
            for source in sources:
                try:
                    source_data = self.scrape_website(source)
                    all_data["sources"]["municipalities"].append(source_data)
                    if source_data["status"] == "success":
                        all_data["safety_updates"].extend(source_data.get("updates", []))
                    self.stats["successful"] += 1
                except Exception as e:
                    logger.error(f"Error scraping {source['name']}: {str(e)}")
                    all_data["sources"]["municipalities"].append(
                        {"name": source["name"], "status": "error", "error": str(e)}
                    )
                    self.stats["failed"] += 1
                self.stats["total_scraped"] += 1
                time.sleep(random.uniform(1, 3))

        # Scrape international sources
        logger.info(f"Scraping international sources...")
        for source in INTERNATIONAL_SOURCES:
            try:
                source_data = self.scrape_website(source)
                all_data["sources"]["international"].append(source_data)
                if source_data["status"] == "success":
                    all_data["safety_updates"].extend(source_data.get("updates", []))
                self.stats["successful"] += 1
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")
                all_data["sources"]["international"].append(
                    {"name": source["name"], "status": "error", "error": str(e)}
                )
                self.stats["failed"] += 1
            self.stats["total_scraped"] += 1
            time.sleep(random.uniform(3, 6))

        # Note: Weibo and WeChat require special API access or cookies
        # This is a placeholder for social media data collection
        all_data["sources"]["social_media"] = {
            "note": "Weibo/WeChat require special API access or custom scraping solutions",
            "weibo_count": len(SOCIAL_MEDIA_SOURCES["weibo"]),
            "wechat_count": len(SOCIAL_MEDIA_SOURCES["wechat"]),
        }

        all_data["statistics"] = self.stats

        logger.info(
            f"Scraping completed. Success: {self.stats['successful']}, Failed: {self.stats['failed']}"
        )

        return all_data

    def scrape_metro_city(self, city_config):
        """Scrape a single Chinese metro city website"""
        result = {
            "name": city_config["name"],
            "city": city_config["city"],
            "url": city_config["url"],
            "status": "pending",
            "updates": [],
            "last_check": datetime.now().isoformat(),
        }

        try:
            response = self.session.get(city_config["url"], timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract news/safety updates from the website
            updates = self.extract_updates_from_page(soup, city_config["name"])
            result["updates"] = updates
            result["status"] = "success"
            result["update_count"] = len(updates)

            logger.info(
                f"Successfully scraped {city_config['name']}: {len(updates)} updates found"
            )

        except requests.exceptions.Timeout:
            result["status"] = "timeout"
            result["error"] = "Connection timeout"
            logger.warning(f"Timeout scraping {city_config['name']}")
        except requests.exceptions.ConnectionError:
            result["status"] = "connection_error"
            result["error"] = "Failed to connect"
            logger.warning(f"Connection error for {city_config['name']}")
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.warning(f"Error scraping {city_config['name']}: {str(e)}")

        return result

    def scrape_website(self, site_config):
        """Scrape a general website"""
        result = {
            "name": site_config["name"],
            "url": site_config["url"],
            "status": "pending",
            "updates": [],
            "last_check": datetime.now().isoformat(),
        }

        try:
            response = self.session.get(site_config["url"], timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract news updates
            updates = self.extract_updates_from_page(soup, site_config["name"])
            result["updates"] = updates
            result["status"] = "success"
            result["update_count"] = len(updates)

            logger.info(
                f"Successfully scraped {site_config['name']}: {len(updates)} updates found"
            )

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.warning(f"Error scraping {site_config['name']}: {str(e)}")

        return result

    def extract_updates_from_page(self, soup, source_name):
        """Extract safety-related updates from a webpage"""
        updates = []

        # Common selectors for news articles
        selectors = [
            "article",
            ".news-item",
            ".article-item",
            ".news-list li",
            ".article-list li",
            '[class*="news"] a',
            '[class*="article"] a',
            ".content a",
            "ul.lists li a",
            'div[class*="list"] a',
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements[:20]:  # Limit to first 20 elements
                    try:
                        # Extract title
                        title_elem = element.find(["h1", "h2", "h3", "h4", "span", "p"])
                        if not title_elem:
                            title_elem = element

                        title = title_elem.get_text().strip() if title_elem else ""

                        # Extract URL
                        url = ""
                        if element.name == "a":
                            url = element.get("href", "")
                        else:
                            link = element.select_one("a[href]")
                            if link:
                                url = link.get("href", "")

                        # Extract date
                        date = ""
                        time_elem = element.select_one("time")
                        if time_elem:
                            date = time_elem.get_text().strip()
                        else:
                            date_elem = element.select_one('[class*="date"]')
                            if date_elem:
                                date = date_elem.get_text().strip()

                        # Filter for safety-related content
                        if title and self.is_safety_related(title):
                            updates.append(
                                {
                                    "title": title[:200],  # Limit title length
                                    "url": url,
                                    "date": date,
                                    "source": source_name,
                                }
                            )

                    except Exception:
                        continue
                break  # Found elements, no need to try other selectors

        return updates

    def is_safety_related(self, text):
        """Check if text contains safety-related keywords"""
        if not text:
            return False

        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.safety_keywords)

    def save_data(self, data, filename=None):
        """Save scraped data to JSON file"""
        if filename is None:
            filename = f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return None


def main():
    """Main execution function"""
    print("=" * 70)
    print("Enhanced Subway Safety Data Scraper")
    print(
        f"Scanning {len(CHINESE_METRO_CITIES)} Chinese cities + international sources"
    )
    print("=" * 70)

    scraper = EnhancedSubwayScraper()

    # Scrape all sources
    scraped_data = scraper.scrape_all_sources()

    # Save the data
    filename = scraper.save_data(scraped_data)

    # Print summary
    print("\n" + "=" * 70)
    print("SCRAPING SUMMARY")
    print("=" * 70)
    print(f"Total sources scraped: {scraped_data['statistics']['total_scraped']}")
    print(f"Successful: {scraped_data['statistics']['successful']}")
    print(f"Failed: {scraped_data['statistics']['failed']}")
    print(f"Safety updates found: {len(scraped_data['safety_updates'])}")
    print(f"Data saved to: {filename}")
    print("=" * 70)


if __name__ == "__main__":
    main()
