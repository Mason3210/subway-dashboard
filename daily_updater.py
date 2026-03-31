import schedule
import time
import logging
import json
from datetime import datetime
from scraper import SubwaySafetyScraper
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("daily_scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class DailySafetyUpdater:
    def __init__(self, dashboard_api_url="http://localhost:5000/api/update-data"):
        self.scraper = SubwaySafetyScraper()
        self.dashboard_api_url = dashboard_api_url

    def run_daily_scraping(self):
        """Run the daily scraping routine"""
        logger.info("Starting daily subway safety data scraping...")

        try:
            # Scrape all sources
            scraped_data = self.scraper.scrape_all_sources()

            # Process and format data for dashboard
            dashboard_data = self.process_scraped_data(scraped_data)

            # Save processed data
            self.save_processed_data(dashboard_data)

            # Update dashboard
            self.update_dashboard(dashboard_data)

            logger.info("Daily scraping completed successfully")

        except Exception as e:
            logger.error(f"Error during daily scraping: {str(e)}")

    def process_scraped_data(self, scraped_data):
        """Process scraped data into dashboard format"""
        processed_data = {
            "global_metrics": {
                "total_incidents": len(scraped_data.get("safety_incidents", [])),
                "recent_updates": self.format_updates(scraped_data.get("updates", [])),
                "data_quality": self.calculate_data_quality(scraped_data),
            },
            "regional_data": self.generate_regional_data(scraped_data),
            "data_sources": self.format_data_sources(scraped_data.get("sources", [])),
            "last_updated": datetime.now().isoformat(),
        }

        return processed_data

    def format_updates(self, updates):
        """Format updates for dashboard display"""
        formatted_updates = []

        for update in updates[:10]:  # Limit to top 10 updates
            formatted_updates.append(
                {
                    "content": f"{update.get('title', '')} - {update.get('summary', '')}",
                    "time": update.get("date", datetime.now().strftime("%Y-%m-%d")),
                    "source": update.get("source", "Unknown"),
                    "url": update.get("url", ""),
                }
            )

        return formatted_updates

    def generate_regional_data(self, scraped_data):
        """Generate regional safety data based on scraped information"""
        # This is a simplified version - in production, you'd analyze the scraped data
        # to determine actual regional safety metrics

        regional_data = {
            "china": {
                "incidents": 0,
                "safety_score": 95,
                "last_update": datetime.now().isoformat(),
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

        # Try to extract regional information from updates
        for update in scraped_data.get("updates", []):
            content = (
                update.get("title", "") + " " + update.get("summary", "")
            ).lower()

            if any(
                keyword in content
                for keyword in ["china", "中国", "beijing", "shanghai"]
            ):
                regional_data["china"]["incidents"] += 1
            elif any(
                keyword in content for keyword in ["japan", "tokyo", "osaka", "日本"]
            ):
                regional_data["japan"]["incidents"] += 1
            elif any(
                keyword in content for keyword in ["europe", "london", "paris", "欧洲"]
            ):
                regional_data["europe"]["incidents"] += 1
            elif any(
                keyword in content
                for keyword in ["america", "new york", "地铁", "america"]
            ):
                regional_data["america"]["incidents"] += 1

        return regional_data

    def format_data_sources(self, sources):
        """Format data sources for dashboard"""
        formatted_sources = []

        for source in sources:
            status = "active" if source.get("status") == "success" else "error"
            formatted_sources.append(
                {
                    "name": source.get("name", "Unknown"),
                    "url": source.get("url", ""),
                    "status": status,
                    "last_check": datetime.now().isoformat(),
                }
            )

        return formatted_sources

    def calculate_data_quality(self, scraped_data):
        """Calculate data quality score"""
        total_sources = len(scraped_data.get("sources", []))
        successful_sources = len(
            [s for s in scraped_data.get("sources", []) if s.get("status") == "success"]
        )

        if total_sources == 0:
            return 0

        return round((successful_sources / total_sources) * 100)

    def save_processed_data(self, data):
        """Save processed data to file"""
        try:
            filename = f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Processed data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")

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
                logger.error(
                    f"Failed to update dashboard: {response.status_code} - {response.text}"
                )

        except Exception as e:
            logger.error(f"Error updating dashboard: {str(e)}")

    def schedule_daily_updates(self):
        """Schedule daily updates at 8:00 AM"""
        # Schedule for 8:00 AM every day
        schedule.every().day.at("08:00").do(self.run_daily_scraping)

        logger.info("Daily updates scheduled for 8:00 AM")

        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def run_once(self):
        """Run the update process once (for testing)"""
        logger.info("Running one-time update...")
        self.run_daily_scraping()


# Main execution
if __name__ == "__main__":
    updater = DailySafetyUpdater()

    # For testing, run once immediately
    updater.run_once()

    # Then start the scheduled updates
    # updater.schedule_daily_updates()
