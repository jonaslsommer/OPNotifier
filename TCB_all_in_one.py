from TCBNotifier import check_contiuous_button
import json
from pathlib import Path
import sys
from asyncio import sleep as sleeep

import discord
from discord import app_commands
from config import TOKEN, GUILD, GUILD_ID

print(TOKEN)
base_path = Path(__file__).resolve().parent
json_path = base_path / "TCB_data" / "data.json"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def periodic_task():
    await client.wait_until_ready()
    while not client.is_closed():
        with open(json_path,"r",encoding="utf-8") as f:
            data = json.load(f)
        temp = await check_contiuous_button(data['newest_known_chapter'])
        print(temp)
        if  temp[0] == data['newest_known_chapter']:
            print("tot")
        else:
            print("holy frickers")
            channel = client.get_channel(1279427281575608380) #1279427281575608380 , 697111670815981581
            embed = discord.Embed(
                title=f":pirate_flag: **CHAPTER __{temp[1]}__ IS OUT** :pirate_flag:",
                color=discord.Color.pink(),
                type="rich"
            )
            embed.add_field(name="Link:", value=f"[Click here]({temp[0]})", inline=False)
            embed.set_image(url=temp[2]) #"https://static0.gamerantimages.com/wordpress/wp-content/uploads/2022/05/Luffy-imitates-Chopper.jpg"
            memberlist = []
            memberlist.append(discord.utils.find(lambda m: m.name == "chopprr", channel.guild.members))
            memberlist.append(discord.utils.find(lambda m: m.name == "saltydave", channel.guild.members))
            memberlist.append(discord.utils.find(lambda m: m.name == "rosensuppe", channel.guild.members))
            memberlist = [member.id for member in memberlist]
            #text = f"<@{memberlist[0]}><@{memberlist[1]}><@{memberlist[2]}>"
            await channel.send(f"<@{memberlist[0]}> <@{memberlist[1]}> <@{memberlist[2]}>",embed=embed)
            jonathan = discord.utils.get(channel.guild.members, id=memberlist[2])  # Replace with the specific user ID
            if jonathan:
                await jonathan.send(embed=embed)
            data['newest_known_chapter'] = temp[0]
            with open(json_path,"w",encoding="utf-8") as f:
                json.dump(data,f)
        print('Finished checking for new chapters')
        await sleeep(60)

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')
	guild = discord.utils.get(client.guilds, name=GUILD)
	print(f'Connected to guild: {guild.name}')
	await tree.sync(guild=discord.Object(id=GUILD_ID))
	client.loop.create_task(periodic_task())

def run_discord_bot():
	client.run(TOKEN)
     
if __name__ == "__main__":
    run_discord_bot()
