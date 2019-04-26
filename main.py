import discord
import asyncio
import re
import constants


bot = discord.Client()

utils = discord.utils

adam_count = 0
cesar_count = 0
troy_count = 0

@bot.event
async def on_message(message):
    author = message.author
    content = message.content
    
    general_text = utils.get(bot.get_all_channels(), type=discord.ChannelType.text, id=constants.TEXT_GENERAL)

    # Checks if the message has a prefix and command
    if re.match(r"^![A-Za-z]+", content):
        args = content.split(None, 1)

        command = args[0][1:].lower()
        options = args[1] if len(args) > 1 else ""

        # Bot repeats message
        if re.match(r"^say$", command) and options:
            if author.id == constants.USER_TREVOR:
                await bot.send_message(general_text, options)
            else:
                await bot.send_message(message.channel, constants.UNAUTHORIZED)
        # Deletes messages in a channel
        elif re.match(r"^(del|delete)$", command) and options.isdigit() and author.id in constants.ADMINS:
            num = int(options)

            # Limits the number of messages that can be deleted at a time
            if num > 10:
                await bot.send_message(message.channel, constants.INVALID_DELETE)
            else:
                async for log in bot.logs_from(message.channel, limit=num + 1):
                    await bot.delete_message(log)
        else:
            await bot.send_message(message.channel, constants.INVALID_COMMAND)
            

@bot.event
async def on_voice_state_update(before, after):
    global adam_count
    global cesar_count
    global troy_count

    user_id = before.id
    channels = before.server.channels
    old_channel = before.voice.voice_channel
    new_channel = after.voice.voice_channel

    # User joins a voice channel
    if old_channel == None and new_channel != None:
        general_channel = utils.find(lambda c: c.id == constants.TEXT_GENERAL, channels)
        voice_channel = utils.get(channels, type=discord.ChannelType.voice, id=new_channel.id)
        members = len(voice_channel.voice_members)

        if user_id == constants.USER_ADAM and members > 1:
            #adam_count += 1
            #if adam_count % 3 == 0:
            await bot.send_message(general_channel, constants.ADAM_JOINS)
        elif user_id == constants.USER_CESAR and members > 1:
            #cesar_count += 1
            #if cesar_count % 4 == 0:
            await bot.send_message(general_channel, constants.CESAR_JOINS)
        elif user_id == constants.USER_TROY and members > 1:
            #troy_count += 1

bot.run(constants.TOKEN)
