How to set up the Voice Chat Notifier Bot.

DISCLAIMER, the Bot can be run on any PC which has python and pip installed (https://www.python.org/downloads/). However, in order for the bot to be effective, it is recommended to have the bot hosted somewhere so that it runs 24/7.

1. Go to https://discord.com/developers and create a new application. Give the bot a name.
2. You'll be provided an Application ID and a Public Key. Note these somewhere safe.
3. On the sidebar, click on OAuth2, then click on the Authorization Method drop down, and choose In-app authorization. A new section called "Scopes" will appear. Tick the "bot" box, and "Bot Permissions" will appear beneath. Tick the following boxes:
   - Manage Roles
   - Manage Channels
   - Manage WebHooks
   - Read Messages/View Channels
   - Send Messages
     
4. On the sidebar, click on "Bot" and then you'll need to set the bot's username. Click on "Reset Token" and copy this long string into a notepad for later on.

5. Within the same section, enable the following switches:
   - Server Members Intent
   - Message Content Intent
     
6. Within the same section, there are Bot Permissions at the bottom, tick on the same boxes wich you did for Step 3
7. At the bottom of the page will be a permissions integer, onces all boxes are ticked, copy this number and hold it in the same notepad as the Bot Token for later on.
8. Enable developer mode on Discord. Go to Settings > Advanced and then enable the Developer Mode switch.

9. Create a role in your Discord server, call it something like "vcnotifs". Then, go to Server Settings > Roles > click the 3 dots next to the role you just created and click "Copy Role ID"
10. Edit the Python script to include the role ID within the variable labelled: notification_role_id. So it should look something like:
    - notification_role_id = 118715923840923409234

11. Create a text channel within your Discord server, call it something like "vc-optin-optout". This will be where users can opt in. Although they could technically use any text channel if they wanted to...
12. Create another text channel, call it something like "vc-notifications". Edit the permissions of this channel so that only the "vcnotifs" role above can see it. Then right click that text channel and copy the channel ID.
13. Edit the Python script to include the text channel ID within the variable labelled: target_channel_id. So it should look something like:
    - target_channel_id = 1187708923470234879523
This will tell the bot to send notifications to the vc-notifications channel, and only users who have opted in (and been assigned the vcnotifs role) will receive the notification.
      
14. Edit the Python script to include the Bot Token you copied earlier. Insert the Token within the client.run function at the bottom of the code, it should look like:
    - client.run('$G"R£059g452g"$5g2$%G"4%G>5542')
      
15. Now you'll need to create a Bot invite link. Go to https://discordjs.guide/preparations/adding-your-bot-to-servers.html#bot-invite-links to learn how to do this. You'll need the following things within your invite link:
    - The Application ID mentioned in step 2
    - The Permissions Interger mentioned in step 7
   
16. Paste the link into a browser, if all works, you should get the typical bot auth page that shows up when adding bots.
17. Once you've added the bot to your server. You'll need to start running the script. Assuming that you either have a server to run the script from, or you've installed Python on your current machine/PC, click on the python file it and should boot.
18. The terminal should advise if the sign-in to the Gateway was successful. You should then see your Discord bot online with the server you added it to.
19. Create another text channel beneath 
20. Type in !optin and !optout within a text channel on your server, the bot should then reply to confirm you've opted in or out aoccrdingly. 
