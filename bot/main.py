import os
import datetime
import discord
from discord.ext import commands, tasks
import cogs

records = {}


def main():
    global records

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="n!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} online")
        cogs.add_cogs(bot, records)
        daily_feed.start()

    @tasks.loop(time=datetime.time(hour=12, tzinfo=datetime.timezone.utc))
    async def daily_feed(self):
        # loop over records
        # for each record, call handlers.get_embeds(record)
        # sequentially send embeds to respective channels

        pass

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
