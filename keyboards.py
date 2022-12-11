from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('/распознать_объекты')
b2 = KeyboardButton('/сгенерировать_qr_код')
b3 = KeyboardButton('/сгенерировать_текст')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(b1, b2, b3)

