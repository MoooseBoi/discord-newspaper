import handlers
import discord
from discord.ext import commands


class Cog(commands.Cog, name="CRUD"):
    def __init__(self, bot, feed_record):
        self.bot = bot
        self.records = feed_record

    @commands.command(name="new")
    async def new(self, ctx):
        self.records[ctx.channel.id] = {}

        embed = discord.Embed().add_field(name="Welcome", value="new feed record created"),
        await ctx.channel.send(embed=embed)

    @commands.command(name="exit")
    async def exit(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel): name = ctx.user.mention
        elif isinstance(ctx.channel, discord.TextChannel): name = ctx.channel.mention
        else: name = ctx.channel.id

        embed = discord.Embed()

        try:
            del self.records[ctx.channel.id]
            embed.add_field(name="Farewell", value=f"closed record for {name}")
        except KeyError:
            embed.add_field(name="Error", value=f"no existing record for {name}"),

        await ctx.channel.send(embed=embed)

    @commands.command(name="add")
    async def add(self, ctx, *args):
        # get channel id
        # get dictionary associated with id
        # check args[0] for existing handle
        # send result embed
        # Exception: Unsupported handler => wrong handler message
        # Exception: wrong args => args error message

        embed = discord.Embed(color=0xbb2222)
        embed.add_field(name="", value="Unimplemented")

        # implement here

        await ctx.channel.send(embed=embed)

    @commands.command(name="remove")
    async def remove(self, ctx, *args):
        # get channel id
        # check args[0] with record[id] for subscribed handle
        # check args[1] with handle options and remove option if exists
        # if no args[1], set False
        # Exception: bad args => bad arguments
        # Exception: no handle => trying to remove none existant handle
        # Exception: no option => trying to remove none existant option from handle

        embed = discord.Embed()

        # implement here

        await ctx.channel.send(embed=embed)

    @commands.command(name="list")
    async def list_feeds(self, ctx):
        # get channel id
        # get record
        # loop over handles in record
        # for each record, stringify the handler options and add as new field
        #   T/F => <handle> is enabled
        #   List => <handle> -> [loop options]
        #
        # Exception: no record => a record was not created for this channel
        # Exception: no handles => the record does not contain any handles (wow! so empty)

        embed = discord.Embed(title="Subscribed Feeds", color=0x4f86c9)

        # implement here

        await ctx.channel.send(embed=embed)
