import discord
# REMEMBER TO TURN ON DEVELOPER MODE WITHIN DISCORD SO YOU CAN COPY THE IDs OF THE TEXT CHANNEL AND ROLES INVOLVED.
# ALSO MAKE SURE TO INSERT THE BOT TOKEN AT THE BOTTOM OF THE CODE.
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True  # To access member roles
intents.message_content = True  # Required for mentions

client = discord.Client(intents=intents)

target_channel_id = TEXT CHANNEL ID GOES HERE.  # Replace with the ID of the text channel E.G. 118897034986753098456
notification_role_id = ROLE ID GOES HERE  # ID of the role for notification opt-in E.G. 118897009834509834590834

opt_in_members = set()  # Store members who have opted in

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:  # Member joined a voice channel
        channel = after.channel
        message = f'{member.mention} has joined {channel.mention}!'

        if member in opt_in_members:
            target_channel = client.get_channel(target_channel_id)
            if target_channel is not None:
                try:
                    # Tag each opted-in member in the target channel
                    for opted_in_member in opt_in_members:
                        message += f" {opted_in_member.mention}"
                    await target_channel.send(message)
                except discord.Forbidden:
                    print(f"Error: Bot cannot send messages in {target_channel.mention}. Check permissions.")
            else:
                print(f"Error: Text channel with ID {target_channel_id} not found.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore the bot's own messages

    if message.content.lower() == '!optin':
        notification_role = discord.utils.get(message.guild.roles, id=notification_role_id) #Calls to the notification_role_id variable at the top to determine what role should be assigned to the user.
        if notification_role is not None:
            await message.author.add_roles(notification_role)
            opt_in_members.add(message.author)
            await message.channel.send(f"You've opted in to receive voice channel notifications.")
        else:
            await message.channel.send("Error: Notification role not found. Please contact server admins.")

    if message.content.lower() == '!optout':
        notification_role = discord.utils.get(message.guild.roles, id=notification_role_id)
        if notification_role is not None:
            await message.author.remove_roles(notification_role)
            opt_in_members.remove(message.author)
            await message.channel.send(f"You've opted out of voice channel notifications.")
        else:
            await message.channel.send("Error: Notification role not found. Please contact server admins.")

client.run('TOKEN GOES HERE')  # Replace with your actual bot token
