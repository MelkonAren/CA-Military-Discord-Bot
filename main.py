# Imports modules
import nextcord
import os
from nextcord.ext import commands, tasks
from keep_alive import keep_alive

# Creates a Discord client instance
intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True

# Sets the prefix for all commands
bot = commands.Bot(command_prefix='!', intents=intents)

# Special role/channel for the bot to use
role_mentioned = {}
channel_mentioned = {}


# gets the default channel
def default_channel(guild):
  channel_id = channel_mentioned.get(guild.id)
  if channel_id:
    channel = guild.get_channel(channel_id)
    if isinstance(channel, nextcord.TextChannel):
      return channel
  else:
    for channel in guild.text_channels:
      if channel.permissions_for(guild.me).send_messages:
        return channel
  return None


# Confirmation message when bot is active, and begins the automatic schedule reminder
@bot.event
async def on_ready():
  if bot.user:
    print(f'{bot.user.name} is ready to go!')
    schedule_reminder.start()
  else:
    print('Bot is ready to go, but bot.user is not defined! Check your code!')


# ---------------------------------------------------------------
# Commands for the bot
@bot.command()
async def list(ctx):
  response = '''My available commands include:
  !list - Displays this message
  !greet - Greets the user
  !apply - Provides the link to the application form
  !set_role - Sets the role to be mentioned when the command is used    Ex: !set_role @role
  !current_role - Displays the current set role
  !set_channel - Sets the channel to be mentioned when the command is used    Ex: !set_channel #channel
  !current_channel - Displays the current set channel
  '''
  await ctx.send(response)


@bot.command()
async def greet(ctx):
  response = 'Hello, I am the friendly Canadian Military bot! type "!list" for a list of my commands!'
  await ctx.send(response)


@bot.command()
async def apply(ctx):
  response = 'https://forces.ca/en/apply-now/'
  await ctx.send(response)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def set_role(ctx, role: nextcord.Role):
  role_mentioned[ctx.guild.id] = role.id
  await ctx.send(f'Role {role.name} has been set as the role to be mentioned!')


@bot.command()
async def current_role(ctx):
  r_id = role_mentioned.get(ctx.guild.id)

  if r_id:
    role = ctx.guild.get_role(r_id)
    await ctx.send(f'The current role is {role.name}')
  else:
    await ctx.send('No role has been set yet!')


@bot.command()
@commands.has_permissions(manage_channels=True)
async def set_channel(ctx, channel: nextcord.TextChannel):
  channel_mentioned[ctx.guild.id] = channel.id
  await ctx.send(f'Channel {channel.name} has been set for notifications!')


@bot.command()
async def current_channel(ctx):
  c_id = channel_mentioned.get(ctx.guild.id)
  if c_id:
    channel = ctx.guild.get_channel(c_id)
    await ctx.send(f'The current channel is {channel.name}')
  else:
    await ctx.send('No channel has been set yet!')


# ---------------------------------------------------------------
# Message every 24 hours to remind people
# ---------------------------------------------------------------
# reminder message that will be sent every 24 hours
async def reminder():
  for guild_id, r_id in role_mentioned.items():
    guild = bot.get_guild(guild_id)

    if guild:
      role = guild.get_role(r_id)
      channel = default_channel(guild)

      if role and channel:
        await channel.send(
            f'------------------------------------------------------------------------------------------------------------------------------\n# {role.mention} DAILY REMINDER: Please apply for the Canadian Military!\nhttps://forces.ca/en/apply-now/\n------------------------------------------------------------------------------------------------------------------------------'
        )


# Schedules reminders
@tasks.loop(hours=24)
async def schedule_reminder():
  await reminder()


# ---------------------------------------------------------------
# Automatically message somebody with the role when they hop onto a game
@bot.event
async def on_presence_update(before, after):

  if before.activities == after.activities:
    return

  r_id = role_mentioned.get(after.guild.id)
  if not r_id:
    return

  role = after.guild.get_role(r_id)
  if not role or role not in after.roles:
    return

  # Had to fix bug where the bot would send a message both for the game and the users discord status

  # Gets the status and the game, so that it can isolate the game
  status = {
      activity.name
      for activity in before.activities
      if isinstance(activity, nextcord.Game) or (hasattr(
          activity, 'type') and activity.type == nextcord.ActivityType.playing)
  }
  status_game = {
      activity.name
      for activity in after.activities
      if isinstance(activity, nextcord.Game) or (hasattr(
          activity, 'type') and activity.type == nextcord.ActivityType.playing)
  }

  # Gets the final status which is the game without the discord status
  final_game = status - status_game

  if final_game:
    # gets the default channel for the server, and sends the message
    channel = default_channel(after.guild)
    if channel:
      for game in final_game:
        try:
          await channel.send(
              f'Hey {after.mention}! instead of playing {game}, please apply for the Canadian Military instead!\nYou will feel so much better about yourself if you signed up instead!\nhttps://forces.ca/en/apply-now/'
          )
        except nextcord.DiscordException as e:
          print(f'Error sending the message: {e}')


# ---------------------------------------------------------------
# Retrieve token from the secrets file
token = os.environ['TOKEN']
keep_alive()
bot.run(token)
