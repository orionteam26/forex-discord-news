import os
import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def send_to_discord(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():
    today = datetime.now().strftime("%d/%m/%Y")

    if not NEWS_API_KEY:
        send_to_discord("❌ Errore: manca il secret NEWS_API_KEY su GitHub.")
        return

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "forex OR EURUSD OR XAUUSD OR USD",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        error = data.get("message", "Errore sconosciuto")
        send_to_discord(f"❌ Errore NewsAPI:\n{error}")
        return

    articles = data.get("articles", [])

    if not articles:
        send_to_discord("⚠️ Nessuna notizia trovata oggi.")
        return

    message = f"📰 NOTIZIE FOREX DEL GIORNO - {today}\n\n"

    for article in articles:
        title = article.get("title", "Senza titolo")
        link = article.get("url", "")
        source = article.get("source", {}).get("name", "Fonte sconosciuta")

        message += f"🔹 {title}\nFonte: {source}\n{link}\n\n"

    message += "⚠️ Fonte dati: NewsAPI"

    send_to_discord(message)

if __name__ == "__main__":
    main()
