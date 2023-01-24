from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('/Распознать_объекты')
b2 = KeyboardButton('/Сгенерировать_QR_код')
b3 = KeyboardButton('/Cгенерировать_текст')

kb = ReplyKeyboardMarkup(resize_keyboard=False)
kb.add(b1).add(b2).add(b3)


