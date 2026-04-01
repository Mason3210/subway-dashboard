#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update Frontend Script
======================

This script reads the scraped news from news_data.json
and updates the index.html with fresh data.

It integrates with the comprehensive_news_aggregator.py
to provide real-time data to the static frontend.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


def load_news_data():
    """Load news from news_data.json"""
    news_file = Path(__file__).parent / "news_data.json"

    if not news_file.exists():
        print("news_data.json not found - will use fallback data")
        return None

    try:
        with open(news_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading news_data.json: {e}")
        return None


def update_index_html(news_data):
    """Update index.html with fresh news data"""
    index_file = Path(__file__).parent / "index.html"

    if not index_file.exists():
        print("index.html not found")
        return False

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        if news_data and "events" in news_data:
            events = news_data["events"]
            print(f"Updating index.html with {len(events)} events")

            # Convert events to JavaScript array format
            events_js = []
            for event in events[:60]:  # Limit to 60 events
                events_js.append(
                    {
                        "id": event.get("id", 0),
                        "time": event.get("time", ""),
                        "title": event.get("title", ""),
                        "source": event.get("source", ""),
                        "category": event.get("category", "news"),
                        "url": event.get("url", "#"),
                        "isNew": event.get("isNew", False),
                        "summary": event.get("summary", ""),
                        "verified": event.get("verified", True),
                    }
                )

            # Create the events string
            events_str = json.dumps(events_js, ensure_ascii=False)
            events_str = events_str.replace("true", "true").replace("false", "false")

            # Update events in index.html
            pattern = r"events:\s*\[.*?\],"
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern, f"events: {events_str},", content, flags=re.DOTALL
                )
                print("Updated events array")
            else:
                print(
                    "Events pattern not found in index.html - manual update may be needed"
                )

            # Update lastUpdated timestamp
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = re.sub(
                r"lastUpdated:\s*new\s+Date\(\)\.toLocaleString\(['\"]zh-CN['\"]\)",
                f"lastUpdated: '{today}'",
                content,
            )

            # Write updated content
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Successfully updated index.html at {today}")
            return True
        else:
            print("No events in news_data - keeping existing data")
            return False

    except Exception as e:
        print(f"Error updating index.html: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("Updating Frontend with Fresh News Data")
    print("=" * 60)

    news_data = load_news_data()

    if news_data:
        print(f"Loaded {news_data.get('total_events', 0)} events from news_data.json")
        print(f"Updated at: {news_data.get('updated_at', 'unknown')}")

    success = update_index_html(news_data)

    if success:
        print("=" * 60)
        print("Frontend update completed!")
        print("=" * 60)
        return 0
    else:
        print("Frontend update skipped or failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
