from settings import *
import asyncpraw
import random


@bot.command()
async def nbameme(ctx):
    reddit = asyncpraw.Reddit(
        client_id="K954-v1jvEol4e5WfVe08g",
        client_secret="b2vXCIM5alA1QIldtnORiXw-6F9U9g",
        user_agent="nbaRedditApi",
    )
    subreddit = await reddit.subreddit("Nbamemes")
    imageLink = await subreddit.random()
    if imageLink.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
        embed = discord.Embed(title=imageLink.title, colour=discord.Colour.random())
        embed.set_image(url=imageLink.url)
        await ctx.send(embed=embed)
        # if verification fails, send out an error message; this may be changed to repeat until it works
    else:
        # makes bot send error message
        await ctx.send("An error has occured, please try again later. Code: sbsusm_verificationFailed")