import os
TOKEN = os.getenv("TOKEN")
import discord
from discord.ext import tasks
import feedparser
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1472955412172243017  

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# 네이버 RSS
RSS_WORLD = "https://news.naver.com/main/rss/feed.naver?mode=LSD&mid=shm&sid1=104"
RSS_KOREA = "https://news.naver.com/main/rss/feed.naver?mode=LSD&mid=shm&sid1=100"

def get_news():
    news_list = []

    for url, label in [(RSS_WORLD, "🌍 세계 시사"), (RSS_KOREA, "🇰🇷 국내 시사")]:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            news_list.append(f"[{label}] {entry.title}\n{entry.link}\n")

    return "\n".join(news_list[:5])

@tasks.loop(minutes=1)
async def daily_news():
    now = datetime.now(ZoneInfo("Asia/Seoul"))

    if now.hour == 9 and now.minute == 0:
        channel = await client.fetch_channel(CHANNEL_ID)
        news = get_news()
        await channel.send(f"📊 오늘의 주요 뉴스 브리핑\n\n{news}")

@client.event
async def on_ready():
    print(f"{client.user} 로그인 완료!")
    daily_news.start()

client.run(TOKEN)

