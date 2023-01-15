from settings import *
from account import *
import requests
import random
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import commonplayerinfo
from datetime import datetime
from PIL import Image

f = open('config.json')
config = json.load(f)
nbaToken = config["nbaToken"]

teams = {
    "Celtics": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Boston_Celtics.svg/800px-Boston_Celtics.svg.png",
    "Nets": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/bkn.png",
    "Knicks": "https://upload.wikimedia.org/wikipedia/en/thumb/2/25/New_York_Knicks_logo.svg/1200px-New_York_Knicks_logo.svg.png",
    "76ers": "https://s.yimg.com/it/api/res/1.2/Y2zIwJoEu_IM6VUVeCYYUw--~A/YXBwaWQ9eW5ld3M7dz0xMjAwO2g9NjMwO3E9MTAw/https://s.yimg.com/cv/apiv2/default/nba/20181217/500x500/76ers_wbg.png",
    "Raptors": "https://cdn.bleacherreport.net/images/team_logos/328x328/toronto_raptors.png",

    "Bulls": "https://upload.wikimedia.org/wikipedia/en/thumb/6/67/Chicago_Bulls_logo.svg/1200px-Chicago_Bulls_logo.svg.png",
    "Cavaliers": "https://content.sportslogos.net/logos/6/222/full/cleveland_cavaliers_logo_primary_2023_sportslogosnet-5369.png",
    "Pistons": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Pistons_logo17.svg/1200px-Pistons_logo17.svg.png",
    "Pacers": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/ind.png",
    "Bucks": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4a/Milwaukee_Bucks_logo.svg/1200px-Milwaukee_Bucks_logo.svg.png",

    "Hawks": "https://upload.wikimedia.org/wikipedia/en/thumb/2/24/Atlanta_Hawks_logo.svg/1200px-Atlanta_Hawks_logo.svg.png",
    "Hornets": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c4/Charlotte_Hornets_%282014%29.svg/1200px-Charlotte_Hornets_%282014%29.svg.png",
    "Heat": "https://i.bleacherreport.net/images/team_logos/328x328/miami_heat.png?canvas=492,328",
    "Magic": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/orl.png",
    "Wizards": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Washington_Wizards_logo.svg/1200px-Washington_Wizards_logo.svg.png",

    "Nuggets": "https://upload.wikimedia.org/wikipedia/en/thumb/7/76/Denver_Nuggets.svg/1200px-Denver_Nuggets.svg.png",
    "Timberwolves": "https://a.espncdn.com/i/teamlogos/nba/500/min.png",
    "Thunder": "https://cdn.nba.com/teams/uploads/sites/1610612760/2021/12/fav.png",
    "Trail Blazers": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/por.png",
    "Jazz": "https://1000logos.net/wp-content/uploads/2018/05/Utah_Jazz_Logo.png",

    "Warriors": "https://upload.wikimedia.org/wikipedia/en/thumb/0/01/Golden_State_Warriors_logo.svg/1200px-Golden_State_Warriors_logo.svg.png",
    "Clippers": "https://s.yimg.com/it/api/res/1.2/gKyPp665PsPlIuWx5UK2WQ--~A/YXBwaWQ9eW5ld3M7dz0xMjAwO2g9NjMwO3E9MTAw/https://s.yimg.com/cv/apiv2/default/nba/20181218/500x500/clippers_wbg.png",
    "Lakers": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/1280px-Los_Angeles_Lakers_logo.svg.png",
    "Suns": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/phx.png",
    "Kings": "https://logos-world.net/wp-content/uploads/2020/05/Sacramento-Kings-logo.png",

    "Mavericks": "https://upload.wikimedia.org/wikipedia/en/thumb/9/97/Dallas_Mavericks_logo.svg/800px-Dallas_Mavericks_logo.svg.png",
    "Rockets": "https://upload.wikimedia.org/wikipedia/en/thumb/2/28/Houston_Rockets.svg/800px-Houston_Rockets.svg.png",
    "Grizzlies": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/mem.png",
    "Pelicans": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0d/New_Orleans_Pelicans_logo.svg/1200px-New_Orleans_Pelicans_logo.svg.png",
    "Spurs": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/sa.png"
}


@bot.command()
async def player(ctx, first, last):
    # NBA player images API
    img = requests.get("http://data.nba.net/data/10s/prod/v1/2022/players.json")
    js = img.json()
    playerID = ""
    plyr = commonplayerinfo.CommonPlayerInfo(player_id='203999')  # Dummy value
    playerFound = False
    data = js['league']['standard']

    # Nba player stats API
    querystring = {"search": f"{first.capitalize()} {last.capitalize()}"}
    headers = {
        "X-RapidAPI-Key": f"{nbaToken}",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }
    stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()

    for pl in data:
        if pl['firstName'].lower() == first.lower() and pl['lastName'].lower() == last.lower():
            playerID = pl['personId']
            plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")
            playerFound = True
    if not playerFound:
        em = discord.Embed(title="Player not Found")
        await ctx.send(embed=em)
    else:
        em = create_embed(stats, playerID, first, last, plyr)
        await ctx.send(embed=em)


@bot.command()
async def rand(ctx):
    # NBA player images API
    img = requests.get("http://data.nba.net/data/10s/prod/v1/2022/players.json")
    js = img.json()
    data = js['league']['standard']
    selectedPlayer = random.choice(data)
    playerID = selectedPlayer['personId']
    plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID }")  # Dummy value
    firstName = selectedPlayer['firstName'].capitalize()
    lastName = selectedPlayer['lastName'].capitalize()

    # Nba player stats API
    querystring = {"search": f"{firstName} {lastName}"}
    headers = {
        "X-RapidAPI-Key": f"{nbaToken}",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }
    stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()
    while not stats['data']:
        selectedPlayer = random.choice(data)
        playerID = selectedPlayer['personId']
        plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")  # Dummy value
        firstName = selectedPlayer['firstName'].capitalize()
        lastName = selectedPlayer['lastName'].capitalize()

        # Nba player stats API
        querystring = {"search": f"{firstName} {lastName}"}
        stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()

    em = create_embed(stats, playerID, firstName, lastName, plyr)
    await ctx.send(embed=em)
    addPlayer(ctx.author.id, f"{firstName} {lastName}")
    if stats['data'][0]['team']['abbreviation'] == "TOR":
        addToBalance(ctx.author.id, 5)
        await ctx.send("Congrats! You got a Toronto Raptors player. You earned $5")


@bot.command()
async def guard(ctx):
    # NBA player images API
    img = requests.get("http://data.nba.net/data/10s/prod/v1/2022/players.json")
    js = img.json()
    data = js['league']['standard']
    selectedPlayer = random.choice(data)
    while str(selectedPlayer['pos']) != "G" and str(selectedPlayer['pos']) != "G-F":
        selectedPlayer = random.choice(data)
    playerID = selectedPlayer['personId']
    plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")  # Dummy value
    firstName = selectedPlayer['firstName'].capitalize()
    lastName = selectedPlayer['lastName'].capitalize()

    # Nba player stats API
    querystring = {"search": f"{firstName} {lastName}"}
    headers = {
        "X-RapidAPI-Key": f"{nbaToken}",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }
    stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()
    while not stats['data']:
        selectedPlayer = random.choice(data)
        playerID = selectedPlayer['personId']
        plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")  # Dummy value
        firstName = selectedPlayer['firstName'].capitalize()
        lastName = selectedPlayer['lastName'].capitalize()

        # Nba player stats API
        querystring = {"search": f"{firstName} {lastName}"}
        stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()

    em = create_embed(stats, playerID, firstName, lastName, plyr)
    await ctx.send(embed=em)


@bot.command()
async def forward(ctx):
    # NBA player images API
    img = requests.get("http://data.nba.net/data/10s/prod/v1/2022/players.json")
    js = img.json()
    data = js['league']['standard']
    selectedPlayer = random.choice(data)
    while str(selectedPlayer['pos']) != "F" and str(selectedPlayer['pos']) != "F-G":
        selectedPlayer = random.choice(data)
    playerID = selectedPlayer['personId']
    plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")  # Dummy value
    firstName = selectedPlayer['firstName'].capitalize()
    lastName = selectedPlayer['lastName'].capitalize()

    # Nba player stats API
    querystring = {"search": f"{firstName} {lastName}"}
    headers = {
        "X-RapidAPI-Key": f"{nbaToken}",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }
    stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()
    while not stats['data']:
        selectedPlayer = random.choice(data)
        playerID = selectedPlayer['personId']
        plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")  # Dummy value
        firstName = selectedPlayer['firstName'].capitalize()
        lastName = selectedPlayer['lastName'].capitalize()

        # Nba player stats API
        querystring = {"search": f"{firstName} {lastName}"}
        stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()

    em = create_embed(stats, playerID, firstName, lastName, plyr)
    await ctx.send(embed=em)


@bot.command()
async def center(ctx):
    # NBA player images API
    img = requests.get("http://data.nba.net/data/10s/prod/v1/2022/players.json")
    js = img.json()
    data = js['league']['standard']
    selectedPlayer = random.choice(data)
    while str(selectedPlayer['pos']) != "C" and str(selectedPlayer['pos']) != "F-C" and str(
            selectedPlayer['pos']) != "C-F":
        selectedPlayer = random.choice(data)
    playerID = selectedPlayer['personId']
    plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")  # Dummy value
    firstName = selectedPlayer['firstName'].capitalize()
    lastName = selectedPlayer['lastName'].capitalize()

    # Nba player stats API
    querystring = {"search": f"{firstName} {lastName}"}
    headers = {
        "X-RapidAPI-Key": f"{nbaToken}",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }
    stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()
    while not stats['data']:
        selectedPlayer = random.choice(data)
        playerID = selectedPlayer['personId']
        plyr = commonplayerinfo.CommonPlayerInfo(player_id=f"{playerID}")  # Dummy value
        firstName = selectedPlayer['firstName'].capitalize()
        lastName = selectedPlayer['lastName'].capitalize()

        # Nba player stats API
        querystring = {"search": f"{firstName} {lastName}"}
        stats = requests.get("https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring).json()

    em = create_embed(stats, playerID, firstName, lastName, plyr)
    await ctx.send(embed=em)


def create_embed(stats, id, first, last, plyr):
    player_dict = plyr.get_dict()
    player_info = player_dict['resultSets'][0]['rowSet'][0]
    player_stats = player_dict['resultSets'][1]
    cur_year = datetime.now().year
    birth_year = player_info[7]
    by = birth_year[0:4]
    age = int(cur_year) - int(by)
    em = discord.Embed(title=f"{first.capitalize()} {last.capitalize()}",
                       colour=choose_color(stats['data'][0]['team']['abbreviation']))
    em.set_thumbnail(
        url=f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{id}.png")

    em.add_field(name="Height (in)", value=f"{player_info[11]}")
    em.add_field(name="Weight (lbs)", value=f"{player_info[12]}", inline=True)
    em.add_field(name="Age", value=f"{age}", inline=True)
    em.add_field(name="Position", value=f"{stats['data'][0]['position']}", inline=False)
    em.add_field(name="Team",
                 value=f"{stats['data'][0]['team']['full_name']} ({stats['data'][0]['team']['abbreviation']})",
                 inline=False)
    em.add_field(name="Conference", value=f"{stats['data'][0]['team']['conference']}")
    em.add_field(name="Division", value=f"{stats['data'][0]['team']['division']}", inline=True)
    return em


def choose_color(team):
    switcher = {
        "ATL": discord.Colour.red(),
        "BKN": discord.Colour.darker_gray(),
        "BOS": discord.Colour.dark_green(),
        "CHA": discord.Colour.teal(),
        "CHI": discord.Colour.dark_red(),
        "CLE": discord.Colour.dark_magenta(),
        "DAL": discord.Colour.dark_blue(),
        "DEN": discord.Colour.dark_gold(),
        "DET": discord.Colour.magenta(),
        "GSW": discord.Colour.gold(),
        "HOU": discord.Colour.brand_red(),
        "IND": discord.Colour.yellow(),
        "LAC": discord.Colour.brand_red(),
        "LAL": discord.Colour.dark_purple(),
        "MEM": discord.Colour.dark_blue(),
        "MIA": discord.Colour.red(),
        "MIL": discord.Colour.dark_green(),
        "MIN": discord.Colour.blue(),
        "NOP": discord.Colour.dark_gray(),
        "NYK": discord.Colour.orange(),
        "OKC": discord.Colour.blue(),
        "ORL": discord.Colour.blue(),
        "PHI": discord.Colour.blue(),
        "PHX": discord.Colour.orange(),
        "POR": discord.Colour.dark_red(),
        "SAC": discord.Colour.purple(),
        "SAS": discord.Colour.dark_gray(),
        "TOR": discord.Colour.red(),
        "UTA": discord.Colour.dark_blue(),
        "WAS": discord.Colour.brand_red()
    }
    return switcher.get(team, discord.Colour.dark_gray)


def create_image(game):
    t1 = Image.open(requests.get(f"{teams[game['awayTeam']['teamName']]}", stream=True).raw)
    t2 = Image.open(requests.get(f"{teams[game['homeTeam']['teamName']]}", stream=True).raw)
    # resize, first image
    t1 = t1.resize((300, 300))
    t2 = t2.resize((300, 300))
    t1_size = t1.size
    new_image = Image.new('RGB', (2 * t1_size[0], t1_size[1]), (250, 250, 250))
    new_image.paste(t1, (0, 0))
    new_image.paste(t2, (t1_size[0], 0))
    new_image.save("thing.png")
    rgba = new_image.convert("RGBA")
    datas = rgba.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
            # storing a transparent value when we find a black colour
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)  # other colours remain unchanged

    rgba.putdata(newData)
    rgba.save("thing.png")


def scores_embed(game):
    create_image(game)
    em = discord.Embed(title=f"{game['awayTeam']['teamTricode']} @ {game['homeTeam']['teamTricode']}",
                       colour=choose_color(game['homeTeam']['teamTricode']))
    file = discord.File("thing.png", filename="thing.png")
    em.set_thumbnail(url="attachment://thing.png")
    em.add_field(name=f"{game['awayTeam']['teamTricode']}: (W-L)",
                 value=f"{game['awayTeam']['wins']}-{game['awayTeam']['losses']}", inline=True)
    em.add_field(name=f"{game['homeTeam']['teamTricode']}: (W-L)",
                 value=f"{game['homeTeam']['wins']}-{game['homeTeam']['losses']}")
    em.add_field(name="Game Status", value=f"{game['gameStatusText']}", inline=False)
    if game['gameStatus'] != 1:
        em.add_field(name="Score", value=f"{game['awayTeam']['score']}-{game['homeTeam']['score']}", inline=False)
        em.add_field(name="Game Leaders", value='\u200b', inline=False)
        em.add_field(name=f"{game['awayTeam']['teamCity']}", value=f"{game['awayTeam']['teamName']}")
        em.add_field(name=f"{game['homeTeam']['teamCity']}", value=f"{game['homeTeam']['teamName']}")
        em.add_field(name='\u200b', value='\u200b', inline=False)
        em.add_field(name=f"{game['gameLeaders']['awayLeaders']['name']}",
                     value=f"> Points: {game['gameLeaders']['awayLeaders']['points']}\n> Assists: {game['gameLeaders']['awayLeaders']['assists']}\n> Rebounds: {game['gameLeaders']['awayLeaders']['rebounds']}")
        em.add_field(name=f"{game['gameLeaders']['homeLeaders']['name']}",
                     value=f"> Points: {game['gameLeaders']['homeLeaders']['points']}\n> Assists: {game['gameLeaders']['homeLeaders']['assists']}\n> Rebounds: {game['gameLeaders']['homeLeaders']['rebounds']}")
    return [em, file]


@bot.command()
async def recap(ctx):
    games = scoreboard.ScoreBoard()

    # dictionary
    dc = games.get_dict()
    live = dc['scoreboard']['games']
    for game in live:
        arr = scores_embed(game)
        await ctx.send(file=arr[1], embed=arr[0])
