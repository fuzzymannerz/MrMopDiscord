<img src="https://i.imgur.com/e6NjKhh.png" alt="Mr. Mop Logo" width="200"/>

# Mr Mop
Open source discord channel cleaning bot.    
Mr. Mop was used on over 10,000 Discord servers daily and had mopped up nearly 40,000,000 messages. Now he's open for everyone!    

https://discord.gg/GqhxktM  


**There is no longer an official hosted Mr. Mop bot.**

# Requirements
* A Registered [Discord App](https://discordapp.com/developers/applications) (Or 2 if you want one for development)
* Python >= 3.3
* Some sort of machine to run it on. VPS/RPi/Old Laptop etc...

# Python Library Requirements
* [Discord.py Rewrite](https://github.com/Rapptz/discord.py/archive/rewrite.zip) (Install the zip via `pip` is easiest)
* asyncio (`pip install asyncio`)

# To Run
1. Change the Discord API tokens (replace the ****) at the bottom of the `mop.py` file.   
```
if devMode:
    bot.run('********')  # DEVELOPMENT TOKEN ONLY!

else:
    # Run the bot using token from Discord developer app page
    bot.run('********')  # PRODUCTION TOKEN ONLY!
```

2. run `mop.py`.

# Reporting Bot Stats to API Sites (Optional)
I won't explain how to do it as you'll have to visit the various sites but they usually require you to join their Discord servers and have a decent bot uptime so if you're just running it on an old laptop at home this probably isn't for you but for those who want it, there is a method included.   

1. Find the line `async def updateBotListAPI():` and uncomment the relevant blocks and fill in the API keys or add in ones as needed.
2. Uncomment the following from the bottom of the file:
```
#if not devMode:
        #bot.loop.create_task(updateBotListAPI())
```
3. Happy days!

# Reporting Problems & Issues
Mr.Mop is no longer going to be maintained by myself but I will accept community additions and pull requests if needed. Please do not contact me on Discord via DM regarding Mr. Mop. It will likely be ignored.    

Having said that, the Mr. Mop Support Server will remain online for discussion of this project at https://discord.gg/GqhxktM
