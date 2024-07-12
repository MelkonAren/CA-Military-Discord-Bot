# CA-Military-Discord-Bot
An independently made Discord Bot that sends out Canadian Military Applications
--> [Try it out!!](https://discord.com/oauth2/authorize?client_id=1258171483398733976&permissions=1126881575824464&integration_type=0&scope=bot) <--

This bot monitors user activities, specifically detecting when a user starts
playing a game, and sends a personalized message encouraging them to apply for the Canadian Military. The bot accurately identifies gaming activities and directs messages by handling presence update events.

## Features
### General Commands
- '!list': Displays a list of every command.
- '!greet': Sends a custom greeting to the user.
- '!apply': Provides a Canadian Military Application website link.
- '!set_role': The user can set a specific role on the server to receive the notifications. (for admins only)
- '!current_role': Displays the current active role for that server.
- '!set_channel': The user can set a specific channel on the server for the bot to message in. (for admins only)
- '!current_channel': Displays the current active channel for that server

### Automated Reminders
- Every 24 hours, the bot will notify all members in the server who possess the specified role in the designated channel to apply for the military.

### Presence Monitoring
- Alongside the daily reminders, any member with the specified role who decides to play a game (that Discord can detect) will receive a personalized message in the designated channel upon exiting the game. Once again, this friendly reminder will ask the user to apply to the military instead of playing games.

## How It Works
### Initialization Features
1. Imports:
- Using 'nextcord.py', 'os', and 'nextcord.ext', the bot can carry out all of its necessary tasks and commands.

2. Prefix:
- The bot uses the constant '!' as the prefix for all commands listed.

### Automated Features
1. Daily Reminders:
- Utilizing the 'schedule_monitoring' task loop, the bot keeps track of the time as soon as it runs to send out updates every day without delay.

2. Presence Monitoring:
- The bot can monitor the statuses of users by comparing the before and after whenever it updates. If the bot tracks that the user merely changed their presence status, the bot will ignore this as it is not a game. However, as soon as the bot detects the user playing a game, it waits for the user to exit the game before sending the message. (You don't want to interrupt the session after all)

### Role and Channel Management:
- A dictionary stores the custom roles and channels that the bot is given with custom IDs so nothing is mixed up.
- With this, every server can have its custom channel/role for the bot to manage.

## Conclusion
The Canadian Military Bot is a great way to keep Discord server members engaged and encourage them to apply to the Canadian Military. With a mix of user commands and automated reminders, it helps maintain consistent and effective communication on the server.
