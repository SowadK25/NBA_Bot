from nbaAPI import *
from settings import *
from account import *
from nbaReddit import *

TOKEN = "MTAxMjM4NzI5MjM5ODIzMTU1Mw.GVFhXO.wBc-FJMJtz2YCYQPRoOGoK1j3F_ycXLD_bhlBQ"


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def test(ctx):
    await ctx.send("Hi sarim")
    em = discord.Embed(title="Cool",
                           colour=discord.Colour.dark_blue())
    em.set_thumbnail(
        url=f"{teams['Mavericks']}")
    # Today's Score Board
    await ctx.send(embed=em)
    games = scoreboard.ScoreBoard()

    # json
    j = games.get_json()
    print(j)

    # dictionary
    d = games.get_dict()
    stuff = d['scoreboard']['games']
    for game in stuff:
        print(game)



bot.run(TOKEN)
