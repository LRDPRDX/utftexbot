#!/usr/bin/env python3

import logging
import time

from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from telebot import types
import telebot

from botex.states import ProcessStates
from botex.middlewares import AntifloodMiddleware
import botex.handlers as handlers
import botex.settings as settings

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler('botex.log')
fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)


bot = telebot.TeleBot(settings.BOT_TOKEN,
                      state_storage=StateMemoryStorage(),
                      parse_mode='MARKDOWN',
                      use_class_middlewares=True)
bot.set_my_description(settings.description)
bot.set_my_commands(settings.commands)

# Filters
bot.add_custom_filter(custom_filters.StateFilter(bot))

# Middlewares
bot.setup_middleware(AntifloodMiddleware(bot, 1))

# Current state
bot.register_message_handler(handlers.state, commands=['state'], pass_bot=True)
bot.register_message_handler(handlers.cancel, state='*', commands=['cancel'], pass_bot=True)
bot.register_callback_query_handler(handlers.cancelQ, func=lambda call: call.data=='/cancel', state='*', pass_bot=True)
bot.register_callback_query_handler(handlers.defaultQ, func=lambda call: True, pass_bot=True)
# Start
bot.register_message_handler(handlers.start, commands=['start'], pass_bot=True)
bot.register_message_handler(handlers.help, commands=['help'], pass_bot=True)
# Ping
bot.register_message_handler(handlers.ping, commands=['ping'], pass_bot=True)
# TeX
bot.register_message_handler(handlers.tex, commands=['tex'], pass_bot=True)
bot.register_message_handler(handlers.texInput, state=ProcessStates.expression, content_types=['text'], pass_bot=True)
bot.register_inline_handler(handlers.texInline, lambda _: True, pass_bot=True)

if __name__ == '__main__' :
    bot.infinity_polling(skip_pending=True,
                         allowed_updates=['message', 'callback_query', 'inline_query'])
