import boto3
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def get_stats(handle):
    for i in range(3):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        try:
            response = s3.get_object(
                Bucket="funny-damon-show-devops",
                Key=f"{handle}_stats_{date}.json"
            )
            return json.loads(response["Body"].read())
        except:
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            try:
                response = s3.get_object(
                    Bucket="funny-damon-show-devops",
                    Key=f"{handle}_stats_{date}.json"
                )
                return json.loads(response["Body"].read())
            except:
                continue
    return None

funny = get_stats("funnydamon")
damon = get_stats("damondylan")

def card(stats, color):
    if not stats:
        return "<p>No data</p>"
    return f"""
    <div class="channel-card">
        <h2 style="color:{color}">{stats['title']}</h2>
        <div class="stats-grid">
            <div class="stat">
                <div class="number" style="color:{color}">{int(stats['subscribers']):,}</div>
                <div class="label">👥 Subscribers</div>
            </div>
            <div class="stat">
                <div class="number" style="color:{color}">{int(stats['views']):,}</div>
                <div class="label">👀 Total Views</div>
            </div>
            <div class="stat">
                <div class="number" style="color:{color}">{stats['videos']}</div>
                <div class="label">🎥 Videos</div>
            </div>
        </div>
    </div>
    """

html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Analytics Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #0f0f0f; color: white; padding: 30px; }}
        h1 {{ text-align: center; font-size: 2em; margin-bottom: 10px; color: #fff; }}
        .updated {{ text-align: center; color: #aaa; margin-bottom: 30px; }}
        .channel-card {{ background: #1a1a1a; border-radius: 15px; padding: 30px; margin: 20px auto; max-width: 700px; }}
        h2 {{ font-size: 1.8em; margin-bottom: 20px; }}
        .stats-grid {{ display: flex; justify-content: space-around; flex-wrap: wrap; gap: 20px; }}
        .stat {{ text-align: center; }}
        .number {{ font-size: 2em; font-weight: bold; }}
        .label {{ color: #aaa; margin-top: 8px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>📊 YouTube Analytics</h1>
    <p class="updated">Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    {card(funny, "#ff0000")}
    {card(damon, "#ff6600")}
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard created: index.html")
