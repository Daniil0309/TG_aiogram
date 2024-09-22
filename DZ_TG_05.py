import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, RAPIDAPI_KEY

# Токены
RAPIDAPI_HOST = "chatgpt-42.p.rapidapi.com"
API_URL = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция для отправки запроса к новому API через RapidAPI
async def get_ai_response(user_message):
    url = API_URL
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "system_prompt": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "web_access": False
    }
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("response", "Извините, не могу ответить.")
    else:
        return "Ошибка при общении с ИИ"


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Напиши мне что-нибудь, и я отвечу с помощью ИИ!")


# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    # Получаем ответ от ИИ
    ai_response = await get_ai_response(message.text)

    # Отправляем ответ пользователю
    await message.answer(ai_response)


# Запуск бота
async def main():
    # Удаляем старые вебхуки и очищаем сессии
    await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



