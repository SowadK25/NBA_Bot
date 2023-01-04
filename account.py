from settings import *
import requests
import json

f = open('config.json')
config = json.load(f)

airtableID = config['airtableID']
airtableTableName = "accounts"
airtableAPIKey = config['airtableToken']
endpoint = f"https://api.airtable.com/v0/{airtableID}/{airtableTableName}"

# request headers
headers = {
    "Authorization": f"Bearer {airtableAPIKey}",
    "Content-Type": "application/json"
}


def addUser(userID):
    data = {
        "records": [
            {
                "fields": {
                    "members": userID,
                    "account_balance": 0,
                    "g1": "empty",
                    "g2": "empty",
                    "f1": "empty",
                    "f2": "empty",
                    "c": "empty"
                }
            }
        ]
    }

    r = requests.post(endpoint, json=data, headers=headers)
    if r.status_code != 200:
        # Error
        return -1
    else:
        return 1


def getData():
    r = requests.get(endpoint, headers=headers)
    if r.status_code != 200:
        # Error
        return -1
    else:
        # No errors, return data in table
        return r.json()


def findUser(userId):
    data = getData()
    if data == -1:
        # Error
        return -1
    else:
        for i in range(len(data['records'])):
            member = str(data['records'][i]['fields']['members'])
            if userId == member:
                return i
        return -2


def getAirtableInfo(userId):
    data = getData()
    userInfo = {
        "airtableId": "",
        "userID": userId,
        "balance": 5,
        "guard1": "",
        "guard2": "",
        "forward1": "",
        "forward2": "",
        "center": ""
    }
    if data == -1:
        # Error
        return -1
    else:
        for i in range(len(data['records'])):
            member = str(data['records'][i]['fields']['members'])
            if userId == member:
                userInfo.update({"airtableId": str(data['records'][i]['id'])})
                userInfo.update({"balance": int(data['records'][i]['fields']['account_balance'])})
                userInfo.update({"guard1": str(data['records'][i]['fields']['g1'])})
                userInfo.update({"guard2": str(data['records'][i]['fields']['g2'])})
                userInfo.update({"forward1": str(data['records'][i]['fields']['f1'])})
                userInfo.update({"forward2": str(data['records'][i]['fields']['f2'])})
                userInfo.update({"center": str(data['records'][i]['fields']['c'])})
                return userInfo
        return -2


@bot.command()
async def bal(ctx):
    member = ctx.author
    userResult = findUser(str(member.id))
    if userResult == -1:
        await ctx.send("An error has occurred. Please try again later")
    elif userResult == -2:
        add = addUser(str(member.id))
        if add == -1:
            await ctx.send("An error has occurred. Please try again later")
        else:
            await ctx.send(f"User {member.display_name} has been added")
            data = getData()
            balance = data['records'][findUser(str(member.id))]['fields']['account_balance']
            await ctx.send(f"You currently have {balance}.")
    else:
        data = getData()
        balance = data['records'][userResult]['fields']['account_balance']
        await ctx.send(f"You currently have {balance}.")


def addToBalance(userId, amount):
    userInfo = getAirtableInfo(str(userId))
    newAmount = int(amount) + userInfo['balance']
    entry = {
        "records": [
            {
                "id": userInfo['airtableId'],
                "fields": {
                    "members": str(userId),
                    "account_balance": int(newAmount)
                },
            }
        ]
    }
    r = requests.patch(endpoint, headers=headers, data=json.dumps(entry))
    if r.status_code != 200:
        # Error
        return -1
    else:
        return 1


def addPlayer(userId, player):
    userInfo = getAirtableInfo(str(userId))
    entry = {
        "records": [
            {
                "id": userInfo['airtableId'],
                "fields": {
                    "g1": str(player),
                },
            }
        ]
    }
    r = requests.patch(endpoint, headers=headers, data=json.dumps(entry))
    if r.status_code != 200:
        # Error
        return -1
    else:
        return 1


# Just for testing
@bot.command()
async def add(ctx, amount):
    addToBalance(ctx.author.id, amount)
    await ctx.send("Added")
