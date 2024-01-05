import discord
import os
import datetime
from discord import Intents

intents = Intents.default()  # Enable all default intents
intents.message_content = True  # Required for reading message content
client = discord.Client(intents=intents)
intents.voice_states = True

# Replace with your Discord bot token
TOKEN = 'MTE4NzA3MzU2MDAyODY0NzQzNA.G3C0rw.C4vGiBbP4b6bvQvS-1ZrRRsz0XMKPcBJ0K-2KM'

# Channel and role IDs
CHANNEL_ID = 1187174405051265054
ROLE_ID = 1187147830985511033

# File to store opted-in member IDs
OPTED_IN_FILE = 'opted_in_members.txt'

# IDs of voice channels to exclude from notifications
EXCLUDED_VOICE_CHANNEL_IDS = [880167821441650748, 979115993609691196]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Load opted-in members from file
    try:
        with open(OPTED_IN_FILE, 'r') as f:
            opted_in_members = set(int(line.strip()) for line in f)
            print('Member added to memory from file')
    except FileNotFoundError:
        opted_in_members = set()

async def opt_out(member, message):
    role = discord.utils.get(member.guild.roles, id=ROLE_ID)
    if role is not None:
        await member.remove_roles(role) # remove_roles is available as a method on the Member class, provided by the discord.py library.
        with open(OPTED_IN_FILE, 'r') as f:
            lines = f.readlines()
        with open(OPTED_IN_FILE, 'w') as f:
            for line in lines:
                if int(line.strip()) != member.id:
                    f.write(line)
        await message.channel.send(f"{member.mention}, you've opted out of voice channel notifications!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '!optin':
        await opt_in(message.author, message)

    if message.content.lower() == '!optout':
        await opt_out(message.author, message)

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and before.channel is not None and after.channel != before.channel:  # Member switched voice channels
        channel = client.get_channel(CHANNEL_ID)
        if channel is not None and after.channel.id not in EXCLUDED_VOICE_CHANNEL_IDS:
            await notify_opted_in(channel, member)

    if after.channel is not None and before.channel is None:  # Member joined a voice channel
        channel = client.get_channel(CHANNEL_ID)
        if channel is not None:
            await notify_opted_in(channel, member)

async def opt_in(member, message):
    opted_in_members = get_opted_in_members()
    if member.id in opted_in_members:
        channel = message.channel # Use the message's channel
        await channel.send(f"{member.mention}, you're already opted in for voice channel notifications!")
        return

    role = discord.utils.get(member.guild.roles, id=ROLE_ID)
    if role is not None:
        await member.add_roles(role)
        with open(OPTED_IN_FILE, 'a', newline='\n') as f:
            f.write(f'\n{member.id}')
        channel = message.channel # Use the message's channel
        await channel.send(f"{member.mention}, You've opted in to voice channel notifications! You'll now receive notifications in {client.get_channel(CHANNEL_ID)}")

async def notify_opted_in(channel, joined_member):
    opted_in_members = get_opted_in_members()
    mention_string = ' '.join(f"<@{member_id}>" for member_id in opted_in_members)
    voice_channel = joined_member.voice.channel  # Get the voice channel
    now = datetime.datetime.now().strftime("%H:%M") # Get current time in HH:MM format
    await channel.send(f"--- \n {joined_member.name} ({joined_member.nick}) has joined {voice_channel.mention}! Time of join: {now}\n \n {mention_string} \n---")

def get_opted_in_members():
    try:
        with open(OPTED_IN_FILE, 'r') as f:
            opted_in_members = set(int(line.strip()) for line in f)
        return opted_in_members
    except FileNotFoundError:
        return set()

client.run(TOKEN)
