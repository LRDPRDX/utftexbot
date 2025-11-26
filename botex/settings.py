from os import environ

from telebot.types import BotCommand

name = "botex"

description = '''
This bot allows you to render math written in a LaTeX-like syntax.
The backend for this bot is this
awesome project: https://github.com/bartp5/libtexprintf . Check it out !

💡 If you have any questions or suggestions feel free to add an issue:
https://github.com/LRDPRDX/utftexbot

☝This bot *doesn't* collect or track *any* data from the users.
I will make the code FOSS when it's done.
'''

commands = [
    BotCommand( 'start'    , 'Let\'s get started !'),
    BotCommand( 'help'     , 'More details'),
    BotCommand( 'ping'     , 'Check if the bot is active'),
    BotCommand( 'tex'      , 'LaTeX -> Message'),
    BotCommand( 'state'    , 'Current state'),
    BotCommand( 'cancel'   , 'Cancel any action (reset your current state)'),
]

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0 :
    logger.error('BOT_TOKEN variable is missing ! Exiting now !')
    exit(1)

# GROUP_ID = environ.get('GROUP_ID', '')
# if len(GROUP_ID) == 0 :
#     logger.error('GROUP_ID variable is missing ! Exiting now !')
#     exit(1)
# GROUP_ID = int(GROUP_ID)
