from commands import discord_command as command
from commands.models import Quote
from random import choice
from time import time
import asyncio

import giphypop
G = giphypop.Giphy()

from keys import discord_app


@command('wizard')
async def wizard(network, channel, message):

    wizards = [
        '`(∩｀-´)⊃━☆ﾟ.･｡ﾟ`',
        '`(⊃｡•́‿•̀｡)⊃━☆ﾟ.･｡ﾟ`',
        '`(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ . * ･ ｡ﾟ`',
        '`(∩ ͡°╭͜ʖ╮͡ ͡°)⊃━☆ﾟ. * ･ ｡ﾟ`',
        '`( ✿ ⊙ ͜ʖ ⊙ ✿ )━☆ﾟ.*･｡ﾟ`',
        '`( ∩ ✿⊙ ͜ʖ ⊙✿)⊃ ━☆ﾟ.*･｡ ﾟ`',
    ]

    await network.send_message(channel, choice(wizards))


@command('shrug')
async def shrug(network, channel, message):
    await network.send_message(channel, '`¯\_(ツ)_/¯`')


@command('shame')
async def shrug(network, channel, message):
    await network.send_message(channel, '`ಠ_ಠ`')


@command('feelsbadfam')
async def feelsbadfam(network, channel, message):
    await network.send_file(channel, 'static/feelsbadfam.png')


@command('youropinion')
async def youropinion(network, channel, message):
    await network.send_file(channel, 'static/youropinion.png')


@command('lewd')
async def lewd(network, channel, message):
    lewds = ['anneLewd1.jpg', 'anneLewd2.gif', 'anneLewd3.png', 'sledgeLewd.gif', 'beanLewd.gif']  # TODO get some randint() action in here
    await network.send_file(channel, 'static/{}'.format(choice(lewds)))


@command('blush')
async def blush(network, channel, message):
    await network.send_file(channel, 'static/anneBlush.png')


@command('neat')
async def neat(network, channel, message):
    verbs = ['dandy', 'glorious', 'hunky-dory', 'keen', 'marvelous', 'neat', 'nifty', 'sensational', 'swell', 'spiffy']

    templates = [
        '{}!',
        'what a {} thing!',
        'that sure is {}!'
    ]

    out = choice(templates).format(choice(verbs))
    await network.send_message(channel, out)


@command('wgaff')
async def wgaff(network, channel, message):
    await network.send_message(channel, '┏(--)┓┏(--)┛┗(--﻿ )┓ WGAFF! ┏(--)┓┏(--)┛┗(--﻿ )┓')


@command('invite')
async def bot_invite(network, channel, message):
    perms = [
        '0x0000400',  # READ_MESSAGES
        '0x0000800',  # SEND_MESSAGES
        '0x0002000',  # DELETE_MESSAGES
        '0x0008000',  # ATTACH_FILES
        '0x0004000',  # EMBED_LINKS ?
        '0x0100000',  # CONNECT (to voice)
        '0x0200000',  # SPEAK
        '0x2000000',  # DETECT VOICE
    ]

    perm_int = sum([int(perm, 0) for perm in perms])

    link = 'https://discordapp.com/oauth2/authorize?&client_id={}&scope=bot&permissions={}'.format(discord_app, perm_int)
    await network.send_message(channel, 'Invite me to your server here: {}'.format(link))


@command('8ball')
async def magicball(network, channel, message):
    responses = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes, definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful",
    ]

    if not message.content.split('8ball')[1]:
        return await network.send_message(channel, 'What do you want me to ask the magic 8 ball?')

    await network.send_message(channel, choice(responses))


@command('giphy')
async def giphy(network, channel, message):
    if not message.content.split('giphy')[1]:
        return await network.send_message(channel, 'What kind of GIF were you looking for?')

    results = G.search(message.content.split('giphy')[1])

    results = [r for r in results][:5]

    if not results:
        await network.send_message(channel, 'I could not find a GIF for that, {}'.format(message.author.name))
    else:
        result = choice(results)
        await network.send_message(channel, result)


@command('help')
@command('halp')
async def help(network, channel, message):
    from commands import Discord_commands as Commands
    cmds = ', '.join(['|{}'.format(k) for k in Commands.keys()])

    await network.send_message(channel, 'I am programmed to respond to the following commands: `{}`'.format(cmds))


@command('quote')
async def quote(network, channel, message):

    if not message.content.split('quote')[1]:
        return await network.send_message(channel, 'Quote who?')

    parts = message.content.split('quote',1)[1].strip().split(' ', 1)

    if len(parts) == 1:
        author = parts[0]
        # return a quote from that user

        if author != 'random':
            pool = [q for q in Quote.filter(author=author)]

        if not pool:
            return await network.send_message(channel, 'I have no quotes from {}'.format(author))

        out = choice(pool)
        return await network.send_message(channel, '#{}: "{}" -- {}'.format(out.id, out.content, out.author))
                
    else:
        # add a quote for that user
        author, quote = parts

        # TODO: guard against malicious quotes, probably?
        new = Quote(author=author, content=quote, timestamp=time())
        new.save()

        return await network.send_message(channel, 'Quote {} added: "{}" -- {}'.format(new.id, new.content, new.author))

