import requests
import asyncio
from aiogram import Bot, Dispatcher, F  # Классы для бота
from aiogram.filters import CommandStart, Command  # Классы для команд
from aiogram.types import Message  # Классы для сообщений
from config import TOKEN  # Импорт токена из config.py

# Токен для OpenWeatherMap API
OPENWEATHER_TOKEN = 'bbc2e3d954b6b7f3bb5f4a87b6a32ecf'


# URL для запроса текущей погоды по городу (здесь Москва по умолчанию)
def get_weather(city: str = 'Moscow'):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_TOKEN}&units=metric&lang=ru'

    try:
        response = requests.get(url, timeout=10)  # Устанавливаем таймаут на 10 секунд
        response.raise_for_status()  # Если статус-код не 200, вызовет исключение

        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        return (f"Погода в {city}:\n"
                f"Температура: {temperature}°C\n"
                f"Описание: {description}\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с")
    except requests.exceptions.Timeout:
        return "Превышено время ожидания ответа от сервера."
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе погоды: {e}"


# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот прогноза погоды. Напиши /weather, чтобы узнать текущую погоду.")


# Команда /help
@dp.message(Command('help'))
async def send_help(message: Message):
    await message.answer("Доступные команды:\n/weather - Показать текущую погоду\n/start - Перезапустить бота")


# Команда /weather для отображения прогноза погоды
@dp.message(Command('weather'))
async def send_weather(message: Message):
    city = 'Moscow'  # Можно изменить на другой город или спрашивать у пользователя
    weather_info = get_weather(city)
    await message.answer(weather_info)


async def main():  # Основная функция
    await dp.start_polling(bot)  # Запуск бота


# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
