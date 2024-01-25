import os
import datetime
import discord
from discord.ext import commands, tasks
import importlib

from dotenv import load_dotenv
load_dotenv()


news_channels = set()


def get_feed_embeds():
    handles = os.listdir("handles")
    embeds = []

    for handle in handles:
        module = f"handles.{handle.replace('.py', '')}"
        try:
            embed = importlib.import_module(module).get_embed()
            embeds.append(embed)
        except AttributeError:
            continue

    return embeds


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

    @bot.command(name="feed")
    async def daily_feed_command(ctx):
        embeds = get_feed_embeds()

        for embed in embeds:
            await ctx.channel.send(embed=embed)

    @tasks.loop(time=datetime.time(hour=12, tzinfo=datetime.timezone.utc))
    async def daily_feed():
        embeds = get_feed_embeds()

        for embed in embeds:
            # initialize channels seperately (lazy load?)
            for id in news_channels:
                channel = bot.get_channel(id)
                await channel.send(embed=embed)

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
