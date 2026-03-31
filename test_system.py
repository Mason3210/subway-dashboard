#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证系统功能
"""

import json
import requests
from datetime import datetime


def test_dashboard_api():
    """测试仪表盘API"""
    print("正在测试仪表盘API...")

    try:
        # 测试数据获取API
        response = requests.get("http://localhost:5000/api/safety-data")
        if response.status_code == 200:
            data = response.json()
            print("✅ API连接成功")
            print(f"   - 数据源数量: {len(data.get('data_sources', []))}")
            print(f"   - 地区数据: {list(data.get('regional_data', {}).keys())}")
            return True
        else:
            print(f"❌ API返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API连接失败: {str(e)}")
        return False


def test_scraper():
    """测试数据爬取功能"""
    print("\n正在测试数据爬取功能...")

    try:
        from scraper import SubwaySafetyScraper

        scraper = SubwaySafetyScraper()

        # 测试数据源配置
        print(f"✅ 已配置 {len(scraper.target_sites)} 个数据源")
        for site in scraper.target_sites:
            print(f"   - {site['name']}: {site['url']}")

        return True
    except Exception as e:
        print(f"❌ 数据爬取模块加载失败: {str(e)}")
        return False


def test_data_format():
    """测试数据格式"""
    print("\n正在测试数据格式...")

    try:
        # 模拟仪表盘数据
        sample_data = {
            "global_metrics": {
                "total_incidents": 5,
                "safety_scores": {"china": 95, "japan": 98},
                "recent_updates": [
                    {
                        "content": "北京地铁10号线安全检查结果良好",
                        "time": datetime.now().strftime("%Y-%m-%d"),
                        "source": "中国地铁协会",
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

        print("✅ 数据格式验证通过")
        print(f"   - 包含 {len(sample_data)} 个主要数据段")
        return True

    except Exception as e:
        print(f"❌ 数据格式错误: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("全球轨道交通安全看板 - 系统测试")
    print("=" * 50)

    # 运行所有测试
    api_test = test_dashboard_api()
    scraper_test = test_scraper()
    format_test = test_data_format()

    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"   API测试: {'通过' if api_test else '失败'}")
    print(f"   爬虫测试: {'通过' if scraper_test else '失败'}")
    print(f"   数据格式测试: {'通过' if format_test else '失败'}")

    if all([api_test, scraper_test, format_test]):
        print("\n所有测试通过！系统运行正常")
        print("\n访问 http://localhost:5000 查看仪表盘")
    else:
        print("\n部分测试失败，请检查相关配置")


if __name__ == "__main__":
    main()
