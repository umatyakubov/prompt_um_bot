import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📸 Promptlar galereyasi",
                    web_app=WebAppInfo(
                        url="https://google.com"
                    )
                )
            ]
        ]
    )

    await message.answer(
        "Xush kelibsiz!\n\nPromptlar galereyasini ochish uchun tugmani bosing.",
        reply_markup=keyboard
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())