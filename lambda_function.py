import boto3
import json
import requests
import os
from datetime import datetime
from googleapiclient.discovery import build

def get_channel_stats(youtube, handle):
    request = youtube.channels().list(
        part="snippet,statistics",
        forHandle=handle
    )
    response = request.execute()
    channel = response["items"][0]
    return {
        "title": channel["snippet"]["title"],
        "subscribers": int(channel["statistics"]["subscriberCount"]),
        "views": int(channel["statistics"]["viewCount"]),
        "videos": channel["statistics"]["videoCount"]
    }

def lambda_handler(event, context):
    api_key = os.environ["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)

    funny = get_channel_stats(youtube, "funnydamon")
    damon = get_channel_stats(youtube, "damondylan")

    date = datetime.now().strftime("%Y-%m-%d")

    # Сохранить в S3
    s3 = boto3.client("s3")
    for name, stats in [("funnydamon", funny), ("damondylan", damon)]:
        filename = f"{name}_stats_{date}.json"
        s3.put_object(
            Bucket="funny-damon-show-devops",
            Key=filename,
            Body=json.dumps(stats, indent=2)
        )

    # Отправить в Telegram
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    message = f"""📊 YouTube Statistics — {date}

🎬 {funny['title']}
👥 Subscribers: {funny['subscribers']:,}
👀 Views: {funny['views']:,}
🎥 Videos: {funny['videos']}

🎬 {damon['title']}
👥 Subscribers: {damon['subscribers']:,}
👀 Views: {damon['views']:,}
🎥 Videos: {damon['videos']}"""

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": message}
    )

    return {"statusCode": 200, "body": "Done!"}
