from googleapiclient.discovery import build
import boto3
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

youtube = build("youtube", "v3", developerKey=API_KEY)

request = youtube.channels().list(
    part="snippet,statistics",
    forHandle="funnydamon"
)

response = request.execute()
channel = response["items"][0]

stats = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "title": channel["snippet"]["title"],
    "subscribers": channel["statistics"]["subscriberCount"],
    "views": channel["statistics"]["viewCount"],
    "videos": channel["statistics"]["videoCount"]
}

print("=== Funny Damon Show - Статистика ===")
print(f"Дата: {stats['date']}")
print(f"Подписчики: {stats['subscribers']}")
print(f"Просмотры: {stats['views']}")
print(f"Видео: {stats['videos']}")

s3 = boto3.client("s3",
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET,
    region_name=AWS_REGION
)

filename = f"stats_{datetime.now().strftime('%Y-%m-%d')}.json"
s3.put_object(
    Bucket="funny-damon-show-devops",
    Key=filename,
    Body=json.dumps(stats, indent=2)
)

print(f"\n✅ Данные сохранены в S3: {filename}")
