from telebot import TeleBot, logger, types, util, formatting

from botex.states import ProcessStates
from botex import messages as M
import botex.keyboards as kb
import botex.logic as logic

def asCode (source: str) -> str :
    return formatting.hcode(source, escape=True)

def asError (source: str) -> str :
    return f'⚠️ {source}'

def expr2text (expr: str) -> str :
    ok, result = logic.latex2string(expr)

    if not ok :
        return asError(result)
    elif not result.strip() :
        return M['no_output']
    else :
        return asCode(result)

def handler(callback) :
    def wrapper(*args, **kwargs) :
        try :
            callback(*args, **kwargs)
        except Exception as e :
            logger.warning(f'Exception raised in a message handler:\n{repr(e)}')
            raise
    return wrapper

# *******************
# ****** STATE ******
# *******************
def doCancel(bot: TeleBot, userID: int, chatID: int) -> None :
    bot.delete_state(userID, chatID)
    bot.send_message(chatID, M['cancel_done'])

@handler
def state(message: types.Message, bot: TeleBot) -> None :
    bot.send_message(message.chat.id, text = f'Your state: {bot.get_state(message.from_user.id, message.chat.id)}')

@handler
def cancel(message: types.Message, bot: TeleBot) -> None :
    doCancel(bot, message.from_user.id, message.chat.id)

@handler
def cancelQ(call, bot: TeleBot) -> None :
    bot.answer_callback_query(call.id, M['cancel'])
    doCancel(bot, call.message.chat.id, call.from_user.id)

@handler
def defaultQ(call, bot: TeleBot) :
    bot.answer_callback_query(call.id, M['query'])
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.delete_state(call.from_user.id, call.message.chat.id)

@handler
def start(message: types.Message, bot: TeleBot) -> None :
    bot.send_message(message.chat.id, text = M['start'], reply_markup=kb.startKeyboard())

@handler
def help(message: types.Message, bot: TeleBot ) -> None :
    bot.send_message(message.chat.id, text = M['help'])

@handler
def notImplemented(message: types.Message, bot: TeleBot) -> None :
    bot.send_message(message.chat.id, text=M['not_implemented'])

@handler
def ping(message: types.Message, bot: TeleBot) -> None :
    bot.send_message(message.chat.id, text='🚀')


# *****************
# ****** TEX ******
# *****************
def render(bot: TeleBot, message: types.Message, expr: str) -> None :
    msg = bot.send_message(message.chat.id, text =M['in_progress'])

    result = expr2text(expr)

    bot.edit_message_text(result, chat_id=message.chat.id, message_id=msg.id, parse_mode='HTML')
    bot.delete_state(message.from_user.id, message.chat.id)

@handler
def tex(message: types.Message, bot: TeleBot) -> None :
    expr = util.extract_arguments(message.text)
    if len(expr) == 0 :
        bot.send_message(message.chat.id, text=M['empty_input'],
                         reply_markup=kb.cancelKeyboard())
        bot.set_state(message.from_user.id, ProcessStates.expression, message.chat.id)
        return
    render(bot, message, expr)

@handler
def texInput(message: types.Message, bot: TeleBot) -> None :
    render(bot, message, message.text)

@handler
def texInline(query: types.InlineQuery, bot: TeleBot) -> None :
    ok, result = logic.latex2string(query.query)
    title = 'Click to render'
    if not ok :
        title = result = asError(result)
    elif not result.strip() :
        title = result = M['no_output']
    else :
        result = asCode(result)

    result = types.InlineQueryResultArticle('tex', title, types.InputTextMessageContent(result, parse_mode='HTML'))
    bot.answer_inline_query(query.id, [result])
