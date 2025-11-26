from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def startKeyboard() :
    markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add('/start', '/help',
               '/ping', '/tex',
               '/state', '/cancel')
    return markup

def cancelKeyboard() :
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('cancel', callback_data='/cancel'))
    return markup
