import logging

from aiogram import Bot, Dispatcher, executor, types

from config import DATABASE_URL, TOKEN, WEB_APP_URL
from db import DB

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db: DB = message.bot.data.get("db")
    await db.add_user(message.from_user.full_name, message.from_user.id)

    await message.bot.send_message(
        text=("Test Web App Bot\n"
              "You can delete your data from "
              "db by sending /delete command "
              "(but then you can't using Web App)."),
        chat_id=message.chat.id,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text="Open Web App",
                    web_app=types.WebAppInfo(url=WEB_APP_URL)
                )
            ]]
        )
    )


@dp.message_handler(commands=['delete'])
async def delete_user_data(message: types.Message):
    db: DB = message.bot.data.get("db")
    await db.delete_user_data(message.chat.id)
    await message.answer(
        "Your data was successfully deleted.\n"
        "To use Web App again send /start command."
    )


async def on_startup(_: Dispatcher):
    bot.data["db"] = await DB.create(DATABASE_URL)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

