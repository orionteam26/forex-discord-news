import os
import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

URL = f"https://newsapi.org/v2/everything?q=forex OR usd OR eur&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"

def send_to_discord(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():

    response = requests.get(URL)
    data = response.json()

    today = datetime.now().strftime("%d/%m/%Y")

    message = f"📰 NOTIZIE FOREX DEL GIORNO - {today}\n\n"

    for article in data["articles"]:

        title = article["title"]
        link = article["url"]

        message += f"🔹 {title}\n{link}\n\n"

    message += "⚠️ Fonte: NewsAPI"

    send_to_discord(message)

if __name__ == "__main__":
    main()
