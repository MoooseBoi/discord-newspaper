import os
import praw
from prawcore import NotFound
import discord

from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
    )


def get_embed(sub_name):
    subreddit = reddit.subreddit(sub_name[2:])

    posts = subreddit.hot(limit=5)
    posts = sorted(posts, key=lambda post: post.score, reverse=True)

    embed = discord.Embed(title=f"{sub_name}", color=0x4f86c9)

    for post in posts:
        link = f"[post](https://www.reddit.com{post.permalink})"

        embed.add_field(inline=False, name=post.title, value=f"{link} | Upvotes: {post.score}")

    return embed


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


def verify_args(args):
    if len(args) != 2:
        return False
    return sub_exists(args[1])
