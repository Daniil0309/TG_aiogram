import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Задание 1: Создание простого меню с кнопками "Привет" и "Пока"
@dp.message(CommandStart())
async def start(message: Message):
    # Создаем клавиатуру с кнопками
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Привет")],
            [types.KeyboardButton(text="Пока")]
        ],
        resize_keyboard=True
    )

    await message.answer("Привет! Выбери одну из опций ниже:", reply_markup=keyboard)


@dp.message(lambda message: message.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(lambda message: message.text == "Пока")
async def say_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Задание 2: Кнопки с URL-ссылками
@dp.message(Command(commands=['links']))
async def send_links(message: Message):
    # Создаем объект InlineKeyboardMarkup с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://news.yandex.ru")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru")],
        [InlineKeyboardButton(text="Видео", url="https://www.youtube.com")]
    ])

    await message.answer("Выберите ссылку:", reply_markup=keyboard)

# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command(commands=['dynamic']))
async def dynamic_keyboard(message: Message):
    # Создаем объект InlineKeyboardMarkup с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Нажмите кнопку ниже:", reply_markup=keyboard)

@dp.callback_query(lambda callback_query: callback_query.data == "show_more")
async def show_more_options(callback: CallbackQuery):
    # Создаем объект InlineKeyboardMarkup с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])
    await callback.message.edit_text("Выберите опцию:", reply_markup=keyboard)

@dp.callback_query(lambda callback_query: callback_query.data in ["option_1", "option_2"])
async def handle_option(callback: CallbackQuery):
    option = "Опция 1" if callback.data == "option_1" else "Опция 2"
    await callback.message.answer(f"Вы выбрали: {option}")

# Основная функция
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


