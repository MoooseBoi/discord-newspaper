import os
import re
import datetime
import feedparser
import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
load_dotenv()


hn_pattern = re.compile(r'<p>Points: (\d+)</p>')
news_channels = set()


def get_hn_embed(query=""):
    url = "https://hnrss.org/frontpage"
    if query != "":
        url += f"?q={query}"

    feed = feedparser.parse(url)

    points = []
    for article in feed.entries:
        points.append((article, int(hn_pattern.findall(article["summary"])[0])))

    results = sorted(points, key=(lambda entry: entry[1]), reverse=True)[:5]
    articles = [result[0] for result in results]

    title = f"Hacker news {query}"
    embed = discord.Embed(title=title, color=0xff3300)

    for article in articles:
        link = f"[article]({article.link})"
        comments = f"[comment section]({article.comments})"

        embed.add_field(inline=False, name=article.title, value=f"{link} | {comments}")

    return embed


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="n!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} online")
        daily_feed.start()

    @bot.command(name="add")
    async def add_channel(ctx):
        news_channels.add(ctx.channel.id)
        print("added ", ctx.channel.id)

    @bot.command(name="rmv")
    async def remove_channel(ctx):
        news_channels.remove(ctx.channel.id)

    @tasks.loop(time=datetime.time(hour=6, minute=30, second=30, tzinfo=datetime.timezone.utc))
    async def daily_feed():
        embed = get_hn_embed()

        for id in news_channels:
            channel = bot.get_channel(id)
            await channel.send(embed=embed)

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
