import os
import datetime
import discord
from discord.ext import commands, tasks
import importlib
import handlers

from dotenv import load_dotenv

load_dotenv()

channels = {}


def main():
    global channels

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="n!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} online")
        daily_feed.start()

    @bot.command(name="init")
    async def init(ctx):
        # consider: should this function even exist?

        # get channel id
        # add id to channels dict with an empty entry
        # Exception: channel exists => do nothing? send error message?

        embed = discord.Embed().add_field(name="Error", value=f"#{ctx.channel.name} already subscribed!")
        if ctx.channel.id not in channels.keys():
            channels[ctx.channel.id] = {}
            embed = discord.Embed().add_field(name="Salutations", value=f"Hello, #{ctx.channel.name}!")
        await ctx.channel.send(embed=embed)

    @bot.command(name="exit")
    async def exit(ctx):
        try:
            del channels[ctx.channel.id]
            embed = discord.Embed().add_field(name="Farewell", value=f"Goodbye, #{ctx.channel.name}!")
        except KeyError:
            embed = discord.Embed().add_field(name="Error", value=f"#{ctx.channel.name} is not subscribed.")
        await ctx.channel.send(embed=embed)

    @bot.command(name="add")
    async def add(ctx, *args):
        # get channel id
        # get dictionary associated with id
        # check args[0] for existing handle
        # send result embed
        # Exception: Unsupported handler => wrong handler message
        # Exception: wrong args => args error message
        try:
            if not handlers.handle_exists(args[0]):
                embed = discord.Embed().add_field(name="Unsupported Handler",
                                                  value=f"{args[0]}'s API is unsupported.")
                await ctx.channel.send(embed=embed)
                return

            handler = importlib.import_module(f"handlers.{args[0]}")

            if not handler.verify_args(args):
                embed = discord.Embed().add_field(name="Bad Argument",
                                                  value=f"Bad argument for {args[0]}!")
                await ctx.channel.send(embed=embed)
                return

            if len(args) == 1:
                channels[ctx.channel.id][args[0]] = True
                embed = discord.Embed().add_field(
                    name="Success", value=f"Succesfully subscribed to {args[0]}")

            else:

                if args[0] in channels[ctx.channel.id].keys():
                    channels[ctx.channel.id][args[0]].add(args[1])
                else:
                    channels[ctx.channel.id][args[0]] = {args[1]}
                embed = discord.Embed().add_field(
                    name="Success", value=f"Subscribed to {args[0]}'s {args[1]}")

        except KeyError or IndexError:
            embed = discord.Embed().add_field(
                name="Error Occurred",
                value="Couldn't subscribe. Are you sure you initialised? ('n!init') | "
                      "Write 'n!help' for available commands.")

        await ctx.channel.send(embed=embed)

    @bot.command(name="remove")  # Unsubscribe
    async def remove(ctx, *args):
        try:
            # If this throws an exception, it means user entered 'n!remove <name>'
            channels[ctx.channel.id][args[0]].remove(args[1])

            if channels[ctx.channel.id][args[0]] == set():
                del channels[ctx.channel.id][args[0]]

            embed = discord.Embed().add_field(name="Success", value=f"Succesfully unsubscribed from {args[0]}'s {args[1]}")

        except (IndexError, AttributeError):
            del channels[ctx.channel.id][args[0]]
            embed = discord.Embed().add_field(name="Success", value=f"Succesfully unsubscribed from {args[0]}")

        except KeyError:
            embed = discord.Embed().add_field(
                name="Error Occurred", value="You are not subscribed to that. Write 'n!help' for available commands.")

        await ctx.channel.send(embed=embed)

    @bot.command(name="list-feeds")
    async def list_feeds(ctx):  # send list of subscribed feeds
        embed = discord.Embed(title=f"__Subscribed Feeds__", color=0x4f86c9)
        try:
            for sub in channels[ctx.channel.id].keys():
                embed.add_field(inline=False, name=sub, value=f"{sub} Subscriptions: {(channels[ctx.channel.id][sub])}")
        except KeyError:
            embed.add_field(inline=False, name="Error!", value="You are not subscribed to anything yet.")
        finally:
            await ctx.channel.send(embed=embed)

    # TO DO - CONFIGURE daily_feed_commands() AND daily_feed() TO ONLY SEND THE STUFF WE SUBSCRIBED TO

    @bot.command(name="feed")
    async def daily_feed_command(ctx):
        embeds = handlers.get_embeds(channels[ctx.channel.id])
        for embed in embeds:
            await ctx.channel.send(embed=embed)

    @tasks.loop(time=datetime.time(hour=12, tzinfo=datetime.timezone.utc))
    async def daily_feed():

        for channel in channels.keys(): # initialize channels seperately (lazy load?)
            embeds = handlers.get_embeds(channels[channel.id])
            for embed in embeds:
                await channel.send(embed=embed)

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
