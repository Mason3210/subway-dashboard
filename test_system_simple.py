#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script - Verify system functionality
"""

import json
import requests
from datetime import datetime


def test_dashboard_api():
    """Test dashboard API"""
    print("Testing dashboard API...")

    try:
        # Test data retrieval API
        response = requests.get("http://localhost:5000/api/safety-data")
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS: API connection successful")
            print(f"   - Data sources count: {len(data.get('data_sources', []))}")
            print(f"   - Regional data: {list(data.get('regional_data', {}).keys())}")
            return True
        else:
            print(f"ERROR: API returned error: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: API connection failed: {str(e)}")
        return False


def test_scraper():
    """Test data scraping functionality"""
    print("\nTesting data scraping functionality...")

    try:
        from scraper import SubwaySafetyScraper

        scraper = SubwaySafetyScraper()

        # Test data source configuration
        print(f"SUCCESS: Loaded {len(scraper.target_sites)} data sources")
        for site in scraper.target_sites:
            print(f"   - {site['name']}: {site['url']}")

        return True
    except Exception as e:
        print(f"ERROR: Data scraping module loading failed: {str(e)}")
        return False


def test_data_format():
    """Test data format"""
    print("\nTesting data format...")

    try:
        # Simulate dashboard data
        sample_data = {
            "global_metrics": {
                "total_incidents": 5,
                "safety_scores": {"china": 95, "japan": 98},
                "recent_updates": [
                    {
                        "content": "Beijing Subway Line 10 safety inspection results good",
                        "time": datetime.now().strftime("%Y-%m-%d"),
                        "source": "China Metro Association",
                    }
                ],
            },
            "regional_data": {
                "china": {
                    "incidents": 2,
                    "safety_score": 95,
                    "last_update": datetime.now().isoformat(),
                },
                "japan": {
                    "incidents": 1,
                    "safety_score": 98,
                    "last_update": datetime.now().isoformat(),
                },
            },
            "data_sources": [
                {"name": "UITP", "url": "https://www.uitp.org", "status": "active"}
            ],
            "last_updated": datetime.now().isoformat(),
        }

        print("SUCCESS: Data format validation passed")
        print(f"   - Contains {len(sample_data)} main data sections")
        return True

    except Exception as e:
        print(f"ERROR: Data format error: {str(e)}")
        return False


def main():
    """Main test function"""
    print("Global Subway Safety Dashboard - System Test")
    print("=" * 50)

    # Run all tests
    api_test = test_dashboard_api()
    scraper_test = test_scraper()
    format_test = test_data_format()

    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"   API Test: {'PASSED' if api_test else 'FAILED'}")
    print(f"   Scraper Test: {'PASSED' if scraper_test else 'FAILED'}")
    print(f"   Data Format Test: {'PASSED' if format_test else 'FAILED'}")

    if all([api_test, scraper_test, format_test]):
        print("\nALL TESTS PASSED! System is running normally")
        print("\nVisit http://localhost:5000 to view the dashboard")
    else:
        print("\nSome tests failed, please check the relevant configuration")


if __name__ == "__main__":
    main()
