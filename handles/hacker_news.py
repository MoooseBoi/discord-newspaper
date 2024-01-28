import discord
import feedparser
import re

points_pattern = re.compile(r'<p>Points: (\d+)</p>')


def get_embed():
    POST_COUNT = 5
    url = "https://hnrss.org/frontpage"
    feed = feedparser.parse(url)

    articles = sorted(feed.entries, key=(lambda article: int(points_pattern.findall(article["summary"])[-1])), reverse=True)[:POST_COUNT]

    embed = discord.Embed(title="Hacker news", color=0xff3300)

    for article in articles:
        link = f"[article]({article.link})"
        comments = f"[comment section]({article.comments})"

        embed.add_field(inline=False, name=article.title, value=f"{link} | {comments}")

    return embed
