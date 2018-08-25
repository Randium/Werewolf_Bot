splash = '''

                    ███████╗██╗  ██╗ ██████╗ ██████╗     ██████╗  ██████╗ ████████╗
                    ██╔════╝██║  ██║██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
                    ███████╗███████║██║   ██║██████╔╝    ██████╔╝██║   ██║   ██║
                    ╚════██║██╔══██║██║   ██║██╔═══╝     ██╔══██╗██║   ██║   ██║
                    ███████║██║  ██║╚██████╔╝██║         ██████╔╝╚██████╔╝   ██║
                    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═════╝  ╚═════╝    ╚═╝

                       - = https://github.com/werewolves-devs/werewolf_bot = -

'''

splashes = [
'It\'s only selling your soul to the devil!',
'They\'re cheap, honest!'
]

import discord
import asyncio
import random
import json
from emoji import emojize, demojize

# Import config data
import config

client = discord.Client()

async def setup_shop(shop_config):
    # Sends the shop message and adds reactions
    embed = discord.Embed(title="Shop (Page 1/1)", description=shop_config["shop_description"], color=0x00ff00)
    for item in shop_config["items"]:
        embed.add_field(name="[{}] {}".format(item["emoji"], item["name"]), value="{} {}\n*{}*\n".format(item["price"], shop_config["currency"], item["description"]), inline=False) # Add item to shop
    message = await client.get_channel(config.shop_channel).send(embed=embed)
    for item in shop_config["items"]:
        await message.add_reaction(emojize(item["emoji"], use_aliases=True)) # Add reactions to shop
    return message # Return the message so we can use it later

async def find_item_from_key(column, query):
    with open('shop.json') as f:
        shop_config = json.load(f) # Load item file
    for item in shop_config["items"]:
        # print("Testing {} against {}".format(item[column], query)) # This is very useful when trying to find the full emoji name of something
        if item[column] == query:
            return item

# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print(' --> Logged in as')
    print('   | > ' + client.user.name)
    print('   | > ' + str(client.user.id))
    # Send shop item message
    await client.get_channel(config.welcome_channel).send('Shop\'s open for business bois')

    with open('shop.json') as f:
        shop_config = json.load(f) # Load shop config file

    shop = await setup_shop(shop_config)

    while True:
        reaction, user = await client.wait_for('reaction_add') # Wait for a user reaction
        if user != client.user and reaction.message.id == shop.id:
            bought_item = await find_item_from_key("emoji", demojize(reaction.emoji))
            await shop.remove_reaction(reaction.emoji, user)
            await client.get_channel(config.shop_channel).send("{} just bought {} for {} {}!".format(user.mention, bought_item["name"], bought_item["price"], shop_config["currency"]))

print(splash)
print(' --> "' + random.choice(splashes) + '"')
print(' --> Please wait whilst we connect to the Discord API...')
try:
    client.run(config.SHOP_TOKEN)
except:
    print('   | > Error logging in. Check your token is valid and you are connected to the Internet.')
