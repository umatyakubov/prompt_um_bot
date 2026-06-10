import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@portfolioum"
CHANNEL_LINK = "https://t.me/portfolioum"
WEBAPP_URL = "https://prompt-um-bot.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def subscribe_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=CHANNEL_LINK)],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ]
    )


def gallery_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📸 Promptlar galereyasi",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )


@dp.message(CommandStart())
async def start_handler(message: Message):
    if await is_subscribed(message.from_user.id):
        await message.answer(
            "Xush kelibsiz!\n\nPromptlar galereyasini ochish uchun tugmani bosing.",
            reply_markup=gallery_keyboard()
        )
    else:
        await message.answer(
            "Galereyadan foydalanish uchun avval kanalga obuna bo‘ling.",
            reply_markup=subscribe_keyboard()
        )


@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        await callback.message.edit_text(
            "✅ Obuna tasdiqlandi!\n\nEndi promptlar galereyasini ochishingiz mumkin.",
            reply_markup=gallery_keyboard()
        )
    else:
        await callback.answer(
            "Hali kanalga obuna bo‘lmagansiz.",
            show_alert=True
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())