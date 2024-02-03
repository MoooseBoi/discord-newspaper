import praw
import discord


def get_embed():
    SUBREDDIT = "worldnews"
    POST_COUNT = 5

    reddit = praw.Reddit(client_id='OCR3d4pvMUxMQ_FCmvpqkg',
                         client_secret='Xdn0LiW8bM6VE-2xKSOFdJcz-1MEOw',
                         user_agent='discord-news-bot-rddit-handler by /u/vorkutavorkutlag')

    subreddit = reddit.subreddit(SUBREDDIT)

    hot_posts = subreddit.hot(limit=POST_COUNT)
    hot_posts = sorted(hot_posts, key=lambda hotpost: hotpost.score, reverse=True)

    embed = discord.Embed(title="World News", color=0x4f86c9)

    for post in hot_posts:
        link = f"[post](https://www.reddit.com{post.permalink})"

        embed.add_field(inline=False, name=post.title, value=f"{link} | Upvotes: {post.score}")

    return embed
