from nbaAPI import *
from settings import *
from account import *
from nbaReddit import *
from nba_api.stats.endpoints import commonplayoffseries

f = open('config.json')
config = json.load(f)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def test(ctx):
    await ctx.send("Hi sarim")
    games = commonplayoffseries.CommonPlayoffSeries()

    # json
    j = games.get_json()
    print(j)
    dc = games.get_dict()
    print(dc)




bot.run(config["botToken"])
