from aiogram import Bot, Dispatcher, executor, types

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

import os 

from functions.object_detection import object_detection
from functions.qr_code import qr_code
from functions.text_generation import text_generation

from keyboards import kb

# Initialize bot and dispatcher 
bot = Bot(token=os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# States
class Object(StatesGroup):
    want = State()
    photo = State()

class Text(StatesGroup):
    want = State()
    text = State()

class QR(StatesGroup):
    want = State()
    link = State()

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)

# Start command handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(chat_id = message.from_user.id,
     text = "Привет, этого бота мы написали специально для пробных уроков, и для того чтобы сдать ресерч Кириллу, и сходить с ним в бар",
      reply_markup=kb)




# Object detection handler
@dp.message_handler(commands=['распознать_объекты'])
async def object_handler(message: types.Message, state: FSMContext):
    await message.reply("Отправь мне фото, и найду на нем объекты")
    await Object.want.set()
    async with state.proxy() as data:
        data['want'] = message.text
    await Object.next()

# Object detection callback handler
@dp.message_handler(state=Object.photo, content_types=['photo'])
async def object_photo_callback(callback: types.Message, state: FSMContext):
    print(callback.chat.id, "Генерирует картинку")
    await callback.photo[-1].download('input.jpg')
    await callback.reply("ИИ ищет объекты...")
    result = object_detection('input.jpg')
    photo = open("output.jpg", 'rb')


    async with state.proxy() as data:
        data['photo'] = callback.photo[-1].file_unique_id


    await bot.send_photo(chat_id=callback.chat.id, photo=photo)
    await state.finish()


# QR code handler
@dp.message_handler(commands=['сгенерировать_qr_код'])
async def qr_code_handler(message: types.Message, state: FSMContext):
    await message.reply("Отправь мне ссылку, и я сгенерирую qr код")
    await QR.want.set()
    async with state.proxy() as data:
        data['want'] = message.text
    await QR.next()

    
@dp.message_handler(state=QR.link, content_types=['text'])
async def qr_code_callback(message: types.Message, state: FSMContext):
    await message.reply("ИИ генерирует qr код...")
    print(message.chat.id, "Генерирует qr код")
    
    async with state.proxy() as data:
        data['link'] = message.text

    result = qr_code(message.text)
    photo = open("qr_code.png", 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await state.finish()

# Text generation handler
@dp.message_handler(commands=['сгенерировать_текст'])
async def text_handler(message: types.Message, state: FSMContext):
    await message.reply("Отправь мне пару слов, и попрошу Шекспира написать что-то похожее")
    await message.reply("ВАЖНО: Шекспир пишет только на английском языке, и он ждет от тебя не более слова на английском языке")
    await Text.want.set()
    async with state.proxy() as data:
        data['want'] = message.text
    await Text.next()
    
@dp.message_handler(state=Text.text, content_types=['text'])
async def text_callback(message: types.Message, state: FSMContext):
    print(message.chat.id, "Генерирует текст")
    await message.reply("ИИ читает Шекспира и генерирует текст...")
    
    async with state.proxy() as data:
        data['text'] = message.text
    await state.finish()

    result = text_generation(message.text)
    for i in range(5):
        await bot.send_message(chat_id=message.chat.id, text=result[i]['generated_text'])


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Я не знаю такой команды, выбери что-то из меню")


# Start long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
