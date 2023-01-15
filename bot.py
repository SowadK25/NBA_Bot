from nbaAPI import *
from settings import *
from account import *
from nbaReddit import *
from nba_api.stats.endpoints import commonplayerinfo

f = open('config.json')
config = json.load(f)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def test(ctx):
    await ctx.send("Hi sarim")
    games = commonplayerinfo.CommonPlayerInfo(player_id='203999')

    # json
    j = games.get_json()
    print(j)
    dc = games.get_dict()
    print(dc['resultSets'][0])
    print(dc['resultSets'][1])
    print(dc['resultSets'][0]['rowSet'][0][7])




bot.run(config["botToken"])
