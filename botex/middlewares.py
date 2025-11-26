from os import environ

from telebot.handler_backends import BaseMiddleware
from telebot.handler_backends import CancelUpdate
from telebot import TeleBot, logger, util

from botex import messages as M
# from botex.settings import GROUP_ID

# This middleware logs every message in the
# chat with the bot. Used for debugging purposes.
# Shouldn't be used in the release. Let's be ethical !
class EchoMiddleware(BaseMiddleware) :
    def __init__(self) :
        super().__init__()
        self.update_types = ['message']

    def pre_process(self, message, data) :
        logger.info(f'from: {message.from_user.id} message: {message.text}')

    def post_process(self, message, data, exception) :
        if exception :
            raise exception

class AntifloodMiddleware(BaseMiddleware) :
    def __init__(self, bot: TeleBot, limit: int) :
        super().__init__()
        self.bot = bot
        self.limit = limit
        self.update_types = ['message']
        self.last_time = {}

    def pre_process(self, message, data) :
        if not message.from_user.id in self.last_time :
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit :
            self.bot.send_message(message.chat.id, M['no_flood'])
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception) :
        if exception :
            raise exception

# This middleware is intended to filter out
# messages from the unknown users: i.e. who
# is not in the member list of the group.
# This ALWAYS MUST BE ADDED to the bot.
# And MUST be the FIRST middleware.
class MemberMiddleware(BaseMiddleware) :
    def __init__(self, bot: TeleBot) :
        super().__init__()
        self.bot = bot
        self.update_types = ['message']

    def pre_process(self, message, data) :
        m = self.bot.get_chat_member(GROUP_ID, message.from_user.id)
        if not m.status in ['member', 'creator', 'administrator'] :
            logger.warning(f'UNKNOWN USER REQUEST: {message.from_user.id}')
            return CancelUpdate()

    def post_process(sefl, message, data, exception) :
        if exception :
            raise exception

class GroupMiddleware(BaseMiddleware) :
    def __init__(self, bot) :
        super().__init__()
        self.bot = bot
        self.update_types = ['message']

    def pre_process(self, message, data) :
        if message.chat.id == GROUP_ID :
            if message.content_type in util.content_type_service :
                return CancelUpdate()
            self.bot.reply_to(message=message, text=M['wrong_chat'])
            return CancelUpdate()

    def post_process(self, message, data, exception) :
        if exception :
            raise
