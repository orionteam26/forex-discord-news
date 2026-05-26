import os
import requests
import feedparser
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

RSS_FEED = "https://rss.fxstreet.com/latest-news"

def send_to_discord(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():

    if not DISCORD_WEBHOOK_URL:
        raise ValueError("Webhook Discord mancante")

    feed = feedparser.parse(RSS_FEED)

    today = datetime.now().strftime("%d/%m/%Y")

    message = f"📰 NOTIZIE FOREX DEL GIORNO - {today}\n\n"

    count = 0

    for entry in feed.entries:

        title = entry.title
        link = entry.link

        message += f"🔹 {title}\n{link}\n\n"

        count += 1

        if count >= 5:
            break

    message += "⚠️ Fonte: FXStreet"

    send_to_discord(message)

if __name__ == "__main__":
    main()
