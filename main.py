import os
import re
import datetime
import feedparser
import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
load_dotenv()


hn_pattern = re.compile(r'<p>Points: (\d+)</p>')
feed_colors = {
    "reddit": 0xff4500,
    "hacker_news": 0xff3300
}


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
    # track urls in json files
    # command for adding, listing and removing urls

    # add integration with different feed types:
    # - reddit
    # - hacker news
    # - add more here :3

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} online")

    @bot.command(name="feed")
    async def feed(context, *args):
        # experimental command to test feed
        news_channel = bot.get_channel(int(os.getenv("NEWS_CH_ID")))
        await news_channel.send(embed=get_hn_embed())

    @tasks.loop(time=datetime.time(hour=8, minute=0))
    async def daily_feed():
        pass

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
