import asyncio
from aiogram import Bot, Dispatcher, F #Классы для бота
from aiogram.filters import CommandStart, Command#Классы для команд
from aiogram.types import Message #Классы для сообщений

from config import TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.text == 'Что такое ИИ?')
async def answer_1(message: Message):
    await message.answer('Искусственный интелект - свойство бота, позволяющее ему вести деятельность, не зная, как она делает это.')

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n/start \n/help')


@dp.message(CommandStart()) #Команда /start
async def cmd_start(message: Message):
    await message.answer('Привет! Я бот!')

async def main(): #Основная функция
    await dp.start_polling(bot) #Запуск бота

if __name__ == "__main__":
    asyncio.run(main())