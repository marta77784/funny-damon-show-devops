import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client("s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

response = s3.get_object(
    Bucket="funny-damon-show-devops",
    Key="stats_2026-03-22.json"
)
stats = json.loads(response["Body"].read())

html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Funny Damon Show - Stats</title>
    <style>
        body {{ font-family: Arial; background: #0f0f0f; color: white; text-align: center; padding: 50px; }}
        h1 {{ color: #ff0000; font-size: 3em; }}
        .card {{ background: #1a1a1a; border-radius: 15px; padding: 30px; margin: 20px; display: inline-block; min-width: 250px; }}
        .number {{ font-size: 2.5em; font-weight: bold; color: #ff0000; }}
        .label {{ color: #aaa; font-size: 1em; margin-top: 10px; }}
    </style>
</head>
<body>
    <h1>Funny Damon Show</h1>
    <p style="color:#aaa">Updated: {stats['date']}</p>
    <div class="card">
        <div class="number">{int(stats['subscribers']):,}</div>
        <div class="label">Subscribers</div>
    </div>
    <div class="card">
        <div class="number">{int(stats['views']):,}</div>
        <div class="label">Total Views</div>
    </div>
    <div class="card">
        <div class="number">{stats['videos']}</div>
        <div class="label">Videos</div>
    </div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard created: index.html")
