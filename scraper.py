import requests
import json
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubwaySafetyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        # Target websites for subway safety information
        self.target_sites = [
            {
                "name": "UITP (国际公共交通协会)",
                "url": "https://www.uitp.org",
                "search_paths": ["/news", "/publications", "/topics/safety"],
                "language": "en",
            },
            {
                "name": "Federal Transit Administration",
                "url": "https://www.transit.dot.gov",
                "search_paths": ["/news", "/safety"],
                "language": "en",
            },
            {
                "name": "中国地铁协会",
                "url": "http://www.mtr.com.cn",
                "search_paths": ["/news", "/safety"],
                "language": "zh",
            },
        ]

        self.safety_keywords = [
            "safety",
            "incident",
            "accident",
            "security",
            "emergency",
            "安全",
            "事故",
            "事件",
            "紧急",
            "安保",
        ]

    def scrape_all_sources(self):
        """Scrape all configured sources for safety information"""
        all_data = {
            "scraped_at": datetime.now().isoformat(),
            "sources": [],
            "safety_incidents": [],
            "updates": [],
        }

        for site in self.target_sites:
            try:
                logger.info(f"Scraping {site['name']}...")
                site_data = self.scrape_site(site)
                all_data["sources"].append(
                    {
                        "name": site["name"],
                        "url": site["url"],
                        "status": "success",
                        "data": site_data,
                    }
                )
                all_data["safety_incidents"].extend(site_data.get("incidents", []))
                all_data["updates"].extend(site_data.get("updates", []))

                # Be respectful with requests
                time.sleep(2)

            except Exception as e:
                logger.error(f"Error scraping {site['name']}: {str(e)}")
                all_data["sources"].append(
                    {
                        "name": site["name"],
                        "url": site["url"],
                        "status": "error",
                        "error": str(e),
                    }
                )

        return all_data

    def scrape_site(self, site_config):
        """Scrape a single website for safety information"""
        site_data = {
            "incidents": [],
            "updates": [],
            "scraped_at": datetime.now().isoformat(),
        }

        base_url = site_config["url"]

        # Try to find safety-related content
        for path in site_config["search_paths"]:
            try:
                url = urljoin(base_url, path)
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")

                # Look for news articles or updates
                articles = self.find_articles(soup, site_config["language"])

                for article in articles[:5]:  # Limit to top 5 articles
                    if self.is_safety_related(
                        article.get("title", "") + " " + article.get("summary", "")
                    ):
                        site_data["updates"].append(
                            {
                                "title": article.get("title", ""),
                                "summary": article.get("summary", ""),
                                "url": article.get("url", ""),
                                "date": article.get("date", ""),
                                "source": site_config["name"],
                            }
                        )

            except Exception as e:
                logger.warning(
                    f"Error scraping path {path} on {site_config['name']}: {str(e)}"
                )
                continue

        return site_data

    def find_articles(self, soup, language):
        """Extract article information from a webpage"""
        articles = []

        # Common selectors for news articles
        selectors = [
            "article",
            ".news-item",
            ".article",
            ".post",
            '[class*="news"]',
            '[class*="article"]',
            'div[class*="item"]',
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements[:10]:  # Limit to first 10 elements
                    article = self.extract_article_info(element, language)
                    if article:
                        articles.append(article)
                break

        return articles

    def extract_article_info(self, element, language):
        """Extract information from a single article element"""
        try:
            # Try to find title
            title_selectors = [
                "h1",
                "h2",
                "h3",
                "h4",
                ".title",
                ".heading",
                '[class*="title"]',
            ]
            title = ""
            for selector in title_selectors:
                title_elem = element.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    break

            if not title:
                return None

            # Try to find summary/description
            summary_selectors = ["p", ".summary", ".description", ".excerpt"]
            summary = ""
            for selector in summary_selectors:
                summary_elem = element.select_one(selector)
                if summary_elem:
                    summary = summary_elem.get_text().strip()[
                        :200
                    ]  # Limit to 200 chars
                    break

            # Try to find URL
            url = ""
            link_elem = element.select_one("a[href]")
            if link_elem:
                url = link_elem.get("href", "")

            # Try to find date
            date = ""
            date_selectors = ["time", ".date", ".published", '[class*="date"]']
            for selector in date_selectors:
                date_elem = element.select_one(selector)
                if date_elem:
                    date_text = date_elem.get_text().strip()
                    # Try to parse date
                    try:
                        if date_elem.get("datetime"):
                            date = date_elem.get("datetime")
                        else:
                            date = date_text
                    except:
                        date = date_text
                    break

            return {"title": title, "summary": summary, "url": url, "date": date}

        except Exception as e:
            logger.warning(f"Error extracting article info: {str(e)}")
            return None

    def is_safety_related(self, text):
        """Check if text contains safety-related keywords"""
        if not text:
            return False

        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.safety_keywords)

    def save_data(self, data, filename="safety_data.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")

    def load_data(self, filename="safety_data.json"):
        """Load previously scraped data"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.info(f"Data file {filename} not found")
            return None
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None


# Example usage and testing
if __name__ == "__main__":
    scraper = SubwaySafetyScraper()

    # Scrape all sources
    logger.info("Starting subway safety data scraping...")
    scraped_data = scraper.scrape_all_sources()

    # Save the data
    scraper.save_data(scraped_data, "scraped_safety_data.json")

    # Print summary
    print(f"Scraping completed at {scraped_data['scraped_at']}")
    print(f"Found {len(scraped_data['safety_incidents'])} safety incidents")
    print(f"Found {len(scraped_data['updates'])} safety updates")
    print(f"Processed {len(scraped_data['sources'])} data sources")
