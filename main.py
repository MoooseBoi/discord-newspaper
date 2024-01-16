import os
import discord
from discord.ext import commands, tasks
import datetime
import feedparser
from dotenv import load_dotenv

load_dotenv()


def get_hn_feed(query=None):
    url = "https://hnrss.org/frontpage"
    if query is not None:
        url += f"?q={query}"

    feed = feedparser.parse(url)

    # evaluate all results
    # find and return highest 3

    for article in feed.entries:
        pass


def get_reddit_feed(subreddit):
    url = ""  # rss feed of given subreddit url

    # get new entries
    # evaluate entries by popularity
    # find and return top 3


def main():
    # track urls in json files
    # command for adding, listing and removing urls

    # add integration with different feed types:
    # - reddit
    # - hacker news
    # - add more here :3

    # cronjob for grabbing the newest feeds every morning:
    #   get top posts from each feed

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} online")

    @bot.command(name="feed")
    async def feed(context, *args):
        # experimental command to test feed

        feed_embed = discord.Embed(title="<Feed name>")
        for i in range(3):
            feed_embed.add_field(inline=False, name=f"{i + 1}. <Title>", value="<summary>\n<link>")

        await context.channel.send(embed=feed_embed)

    @tasks.loop(time=datetime.time(hour=8, minute=0))
    async def daily_feed():
        # get top 3 result of each feed in feeds file
        # create embed for each feed
        # send all embeds in #news channel (os.getenv("news_id"))

        pass

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
