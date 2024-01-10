import discord
import json

with open("token.txt", 'r', encoding="utf8") as tokenfile:
    token = tokenfile.read().strip()

with open("strings.json", 'r', encoding="utf8") as stringsfile:
    strings = json.load(stringsfile)
    strings["joincolor"] = discord.Color(0).from_rgb(*strings["joincolor"])
    strings["leavecolor"] = discord.Color(0).from_rgb(*strings["leavecolor"])

bot = discord.Bot(intents=discord.Intents.default())

async def messageSender(member: discord.Member, channel, join: bool):
    if not isinstance(channel, discord.VoiceChannel):
        return
    
    else:
        if join:
            type = "join"
        else:
            type = "leave"

        embed = discord.Embed(color=strings[type+"color"])
        embed.set_author(name=strings[type].format(member.display_name, channel.name), icon_url=member.avatar.url)

        try:
            await channel.send(embed=embed)
        except:
            pass

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel != after.channel:
        
        if before.channel is not None:
            await messageSender(member, before.channel, False)
        
        if after.channel is not None:
            await messageSender(member, after.channel, True)

bot.run(token)