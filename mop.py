####################################################
#  Mr. Mop | Open Source                           #
#  Copyright (C) 2019  FuzzyTek / Fuzzy Mannerz    #
#  <https://github.com/fuzzymannerz/MrMopDiscord>  #
###########################################################################
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public licenses     #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################

import asyncio
import discord
import requests
import time
from discord.ext import commands
import threading

#####################################################
devMode = False  # IMPORTANT! CHANGE WHEN DEVELOPING!
#####################################################

version = "1.9.0" # Format: Major.Minor.BugFix
lastUpdated = "31 Oct 2019"

# Set the bot description
description = 'A simple Discord message cleaner.'

if devMode:
    cmdPrefix = '*'  # Set the prefix for commands. Default is "/".
else:
    cmdPrefix = '/'  # Set the prefix for commands. Default is "/".

profileImage = "https://i.imgur.com/e6NjKhh.png"
supportServerURL = "https://discord.gg/GqhxktM"

bot = commands.AutoShardedBot(command_prefix=cmdPrefix, description=description,
                              activity=discord.Game(name='{}help'.format(cmdPrefix)))

# Set buffer for total amount of mopped messages
totalMopped = 0


# Set some setting things
embedFooter = 'Mr. Mop Open Source v{} | {}help to view commands. | https://mrmop.ml'.format(version, cmdPrefix)
genericError = 'An error has occurred!'
enjoyText = "Mr. Mop is now open source!\nVisit [https://mrmop.ml](https://mrmop.ml)"

# Set the bot permissions for invite links
perms = "93184"

# Get the current time
currentTime = time.strftime("%H:%M", time.gmtime())

# Bot uptime stats
startTime = time.time()


def formatTime(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd %dh %dm %ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh %dm %ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm %ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)


def upTime():
    return formatTime(time.time() - startTime)


# Remove default help command
bot.remove_command('help')


# Save and retrieve total mopped data // Default for 1.8 = 15,400,000
def saveMop(number):
    global totalMopped
    totalMopped = (totalMopped + number)

    with open(r'mopCount.txt', 'r+') as f:
        value = int(f.read())
        f.seek(0)
        f.write(str(value + number))
        f.close()

    if not devMode:
        totalMopped = (totalMopped + number)

        with open(r'mopCount.txt', 'r+') as f:
            value = int(f.read())
            f.seek(0)
            f.write(str(value + number))
            f.close()


def readMop():
    with open(r'mopCount.txt', 'r+') as f:
        value = int(f.read())
        f.close()
        # return "{:,}".format(value)
        return value


# Set initial total mopped amount
totalMopped = readMop()


# Function to save server errors log
#def PrintServerError(ctx, err):
#    if not devMode:
#        with open(r'logs/serverErrors.log', 'r+') as f:
#            f.write(ctx.guild.name + " | Error: " + err + "\n")
#            f.close()


# Info command
@bot.command()
async def info(ctx):
    try:
        application_info = await bot.application_info()
        serverCount = len(bot.guilds)
        uptime = upTime()

        e = discord.Embed(title='Bot Information & Statistics', colour=0x42cef4)

        e.set_footer(text=embedFooter)

        e.set_thumbnail(url=profileImage)

        e.add_field(name='Mr. Mop Version', value=version)
        e.add_field(name='Discord Version', value=discord.__version__)
        e.add_field(name='Bot Username', value=application_info.name)
        e.add_field(name='Bot ID', value=application_info.id)
        e.add_field(name='Connected Servers', value=str(serverCount))
        e.add_field(name='Latency (in seconds)', value=bot.latency)
        e.add_field(name='Mr. Mop\'s Current Shift', value=uptime)
        e.add_field(name='Server Owner', value=ctx.guild.owner)
        e.add_field(name='Total Mopped Messages', value="{:,}".format(totalMopped))
        e.add_field(name="Bot Last Updated", value=lastUpdated)
        e.add_field(name="Version Changes", value="[https://mrmop.ml](https://mrmop.ml)")

        e.add_field(name="\u200b", value="\u200b")
        e.add_field(name="\u200b", value="\u200b")

        e.add_field(name="Enjoying Mr. Mop?", value=enjoyText)

        await ctx.channel.send(embed=e)

    except Exception as e:
        await ctx.channel.send(genericError)
        PrintServerError(ctx, e)
        return


# Help command
@bot.command()
async def help(ctx):
    try:
        e = discord.Embed(colour=0x42cef4)
        e.set_footer(text=embedFooter)

        e.set_author(name='Mr. Mop Help', icon_url=profileImage)
        e.set_thumbnail(url=profileImage)

        e.add_field(name='Clean up x messages (max 25)', value='```{}mop [x]```'.format(cmdPrefix))
        e.add_field(name='Clean up to 100 current channel messages', value='```{}megamop```'.format(cmdPrefix))
        e.add_field(name='Show the help text', value='```{}help```'.format(cmdPrefix), inline=False)
        e.add_field(name='Show bot invite URL', value='```{}invite```'.format(cmdPrefix), inline=False)
        e.add_field(name='View bot information & statistics', value='```{}info```'.format(cmdPrefix), inline=False)

        e.add_field(name="\u200b", value="\u200b")
        e.add_field(name="\u200b", value="\u200b")

        e.add_field(name="Enjoying Mr. Mop?", value=enjoyText)

        await ctx.channel.send(embed=e)

    except Exception as e:
        await ctx.channel.send(genericError)
        PrintServerError(ctx, e)
        return


# Invite command
@bot.command()
async def invite(ctx):
    try:
        e = discord.Embed(colour=0x42cef4,
                          url='https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}'.format(
                              bot.user.id, perms))
        e.set_footer(text=embedFooter)

        e.set_author(name='Mr. Mop\'s Party Invitation', icon_url=profileImage)
        e.set_thumbnail(url=profileImage)

        e.add_field(name='Invite Link',
                    value='You can invite Mr. Mop to another server using the following URL:\n**https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}**'.format(
                        bot.user.id, perms))

        e.add_field(name="\u200b", value="\u200b")
        e.add_field(name="\u200b", value="\u200b")

        e.add_field(name="Enjoying Mr. Mop?", value=enjoyText)

        await ctx.channel.send(embed=e)

    except Exception as e:
        await ctx.channel.send(genericError)
        PrintServerError(ctx, e)
        return

## Check if the message is pinned or not and return FALSE if it is so as to not delete it during checks
def checkPinned(m):
    if m.pinned == False:
        return True
    else:
        return False

# Remove last 100 messages regardless of sender (bot or otherwise)
@bot.command()
# Add a 10 second cooldown between mops
@commands.cooldown(1, 10, commands.BucketType.guild)
@commands.bot_has_permissions(manage_messages=True)
async def megamop(ctx):
    try:

        canClean = False

        # Check the user has permissions to do the cleanup ("Cleaner" Role OR manage messages permission for current channel)
        for role in ctx.message.author.roles:
            if role.name == "Cleaner":
                canClean = True

        if ctx.author.permissions_in(ctx.channel).manage_messages == True:
            canClean = True

        if canClean == True:
            await ctx.channel.send(
                "**<@{}> has instructed a mega mop cleanup! Please wait...**".format(ctx.message.author.id))
            await asyncio.sleep(3)
            mopped = await ctx.channel.purge(limit=100, check=checkPinned)

            if not devMode:
                saveMop(len(mopped))  # Save mop stats
        else:
            await ctx.channel.send(
                "Sorry <@{}>, but to do that, you'll need the \"Manage Messages\" permission for this channel.".format(
                    ctx.message.author.id))
            await ctx.message.delete()
            raise RuntimeError("Invalid permissions for megamop command.")

    except RuntimeError as e:
        PrintServerError(ctx, e)
        return


@bot.command()
# Add a 10 second cooldown between mops
@commands.cooldown(1, 10, commands.BucketType.guild)
@commands.bot_has_permissions(manage_messages=True)
async def mop(ctx, number):
    try:
        canClean = False

        # Check the user has permissions to do the cleanup ("Cleaner" Role OR manage messages permission for current channel)
        for role in ctx.message.author.roles:
            if role.name == "Cleaner":
                canClean = True

        if ctx.author.permissions_in(ctx.channel).manage_messages == True:
            canClean = True

        if canClean == True:

            # Limit standard mop to 25 messages.
            if int(number) > 25:
                limit = 25
            else:
                limit = int(number)

            await ctx.message.delete()
            await ctx.channel.send(
                "**<@{}> has instructed a cleanup on aisle {}! Please wait...**".format(ctx.message.author.id, limit))
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=limit + 1, check=checkPinned)
            if not devMode:
                saveMop(limit + 1)  # Save mop stats

        if not canClean:
            await ctx.channel.send(
                "Sorry <@{}>, but to do that, you'll need the \"Manage Messages\" permission for this channel.".format(
                    ctx.message.author.id))
            await ctx.message.delete()
            raise RuntimeError("Invalid permissions for megamop command.")

    except RuntimeError as e:
        PrintServerError(ctx, e)
        return


# Update the discordbots.org page with total server count
async def updateBotListAPI():
    while not bot.is_closed():

        # Update discordbots.org count
        #dboauthToken = "********"
        #dbourl = "https://discordbots.org/api/bots/********/stats"
        #dboheaders = {'content-type': 'application/json', 'Authorization': dboauthToken}
        #dbor = requests.post(dbourl, json={"server_count": (len(bot.guilds))}, headers=dboheaders)
        #if dbor.status_code != 200:
        #    print("ERROR connecting to discordbots.org API!\n")

        # Update discord.bots.gg count
        #dbGGoauthToken = "********"
        #dbGGourl = "https://discord.bots.gg/api/v1/bots/********/stats"
        #dbGGoheaders = {'content-type': 'application/json', 'Authorization': dbGGoauthToken}
        #dbGGor = requests.post(dbGGourl, json={"guildCount": (len(bot.guilds))}, headers=dbGGoheaders)
        #if dbGGor.status_code != 200:
        #    print("ERROR connecting to discord.bots.gg API!\n")

        # Update discord.boats count
        #dBoatsoauthToken = "********"
        #dBoatsourl = "https://discord.boats/api/bot/********"
        #dBoatsoheaders = {'content-type': 'application/json', 'Authorization': dBoatsoauthToken}
        #dBoatsor = requests.post(dBoatsourl, json={"server_count": (len(bot.guilds))}, headers=dBoatsoheaders)
        #if dBoatsor.status_code != 200:
        #    print("ERROR connecting to discord.boats API!\n")

        # Update botsfordiscord.com count
        #bfdauthToken = "********"
        #bfdurl = "https://botsfordiscord.com/api/bot/********"
        #bfdheaders = {'content-type': 'application/json', 'authorization': bfdauthToken}
        #bfdr = requests.post(bfdurl, json={"server_count": (len(bot.guilds))}, headers=bfdheaders)

        # if bfdr.status_code != 200:
        #    print("ERROR connecting to botsfordiscord.com API!\n")
        # else:
        #    print("\x1b[1;37;40m\nSuccessfully connected to botsfordiscord.com API.\n")

        #for t in range(1200, -1, -1):  # Wait 20 minutes and update again
            # timeLeft = "{:02d}:{:02d}".format(*divmod(t, 60))
            # print(" Refreshing in {}".format(timeLeft), end="\r")
        #    await asyncio.sleep(1)
        #    continue


# Deal with cooldown errors.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        try:
            await ctx.channel.send(
                "You need to wait at least 10 seconds between server mops <@{}>. Try again shortly.".format(
                    ctx.message.author.id))
            return
        except:
            pass
    if isinstance(error, commands.BotMissingPermissions):
        try:
            await ctx.channel.send(
                "Sorry <@{}>, but I need the \"Manage Messages\" permission for this channel to be able to do that.".format(
                    ctx.message.author.id))
            return
        except:
            pass
    else:
        pass


# Stop bot responding to other bots
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await bot.process_commands(message)


# Print login information to the server console
@bot.event
async def on_ready():
    print("\nLogged in as: [{}] | User ID: [{}] | Start time: [{}]\n".format(bot.user.name, bot.user.id,
                                                                             currentTime))

    #if not devMode:
        #bot.loop.create_task(updateBotListAPI())


if devMode:
    bot.run('********')  # DEVELOPMENT TOKEN ONLY!

else:
    # Run the bot using token from Discord developer app page
    bot.run('********')  # PRODUCTION TOKEN ONLY!
