import boto3
import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

filename = f"stats_{datetime.now().strftime('%Y-%m-%d')}.json"
response = s3.get_object(Bucket="funny-damon-show-devops", Key=filename)
stats = json.loads(response["Body"].read())

message = f"Funny Damon Show\nDate: {stats['date']}\nSubscribers: {int(stats['subscribers']):,}\nViews: {int(stats['views']):,}\nVideos: {stats['videos']}"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": message}
)

print("Sent to Telegram!")
