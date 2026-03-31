from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime, timedelta
import logging
import random

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Sample data structure for subway safety metrics
class SafetyData:
    def __init__(self):
        self.data = {
            "global_metrics": {
                "total_incidents": 0,
                "safety_scores": {},
                "recent_updates": self._generate_sample_updates(),
            },
            "regional_data": {
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
                "hk": {
                    "incidents": 0,
                    "safety_score": 98,
                    "last_update": datetime.now().isoformat(),
                },
            },
            "data_sources": self._generate_data_sources(),
        }

    def _generate_sample_updates(self):
        updates_zh = [
            {
                "time": "2024-01-15",
                "title": "北京地铁启动冬季安全检查",
                "source": "北京地铁",
                "type": "安全",
            },
            {
                "time": "2024-01-14",
                "title": "交通运输部发布最新安全预警",
                "source": "交通运输部",
                "type": "政策",
            },
            {
                "time": "2024-01-14",
                "title": "上海地铁1号线运营调整通知",
                "source": "上海地铁",
                "type": "运营",
            },
            {
                "time": "2024-01-13",
                "title": "广州地铁开展应急演练",
                "source": "广州地铁",
                "type": "演练",
            },
            {
                "time": "2024-01-12",
                "title": "港铁获得年度安全卓越奖",
                "source": "港铁",
                "type": "荣誉",
            },
            {
                "time": "2024-01-11",
                "title": "深圳地铁5号线安全整改完成",
                "source": "深圳地铁",
                "type": "安全",
            },
            {
                "time": "2024-01-10",
                "title": "成都地铁推出智慧运维系统",
                "source": "成都地铁",
                "type": "运营",
            },
            {
                "time": "2024-01-09",
                "title": "杭州亚运期间地铁安全运营",
                "source": "杭州地铁",
                "type": "安全",
            },
        ]
        updates_en = [
            {
                "time": "2024-01-15",
                "title": "Beijing Metro launches winter safety inspection",
                "source": "Beijing Metro",
                "type": "Safety",
            },
            {
                "time": "2024-01-14",
                "title": "Ministry of Transport issues latest safety warning",
                "source": "MOT",
                "type": "Policy",
            },
            {
                "time": "2024-01-14",
                "title": "Shanghai Metro Line 1 operation adjustment notice",
                "source": "Shanghai Metro",
                "type": "Operation",
            },
            {
                "time": "2024-01-13",
                "title": "Guangzhou Metro conducts emergency drill",
                "source": "Guangzhou Metro",
                "type": "Drill",
            },
            {
                "time": "2024-01-12",
                "title": "MTR wins annual safety excellence award",
                "source": "MTR",
                "type": "Award",
            },
        ]
        return random.choice([updates_zh, updates_en])

    def _generate_data_sources(self):
        sources = []
        # Metro companies
        metros = [
            "北京地铁",
            "上海地铁",
            "广州地铁",
            "深圳地铁",
            "成都地铁",
            "杭州地铁",
            "武汉地铁",
            "西安地铁",
            "重庆轨道",
            "天津地铁",
        ]
        for metro in metros:
            sources.append({"name": metro, "url": "#", "status": "active"})

        # Government
        gov = ["交通运输部", "应急管理部", "中国城市轨道交通协会"]
        for g in gov:
            sources.append({"name": g, "url": "#", "status": "active"})

        # International
        sources.append(
            {"name": "UITP", "url": "https://www.uitp.org", "status": "active"}
        )
        sources.append(
            {"name": "MTR HK", "url": "https://www.mtr.com.hk", "status": "active"}
        )

        return sources

    def get_dashboard_data(self):
        return self.data

    def update_data(self, new_data):
        self.data.update(new_data)
        logger.info("Safety data updated")


safety_data = SafetyData()


@app.route("/")
def dashboard():
    return render_template("mtr_dashboard.html")


@app.route("/api/safety-data")
def get_safety_data():
    return jsonify(safety_data.get_dashboard_data())


@app.route("/api/update-data", methods=["POST"])
def update_safety_data():
    try:
        data = request.get_json()
        safety_data.update_data(data)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        safety_data.data["last_updated"] = current_time
        return jsonify({"status": "success", "message": "Data updated successfully"})
    except Exception as e:
        logger.error(f"Error updating data: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
