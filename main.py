import os
from dotenv import load_dotenv
from tabulate import tabulate
from aiogram import Bot, Dispatcher, executor, types

from models import User
from notion import NotionClient

load_dotenv('.env')

bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher(bot)
notion = NotionClient(os.getenv("NOTION_TOKEN"), os.getenv("DB_ID"))

users = []

HELP_MSG = '''
•/start: Start the bot and receive the first movie recommendation.
•/recommend: Receive a new movie recommendation.
•/list: Get a list of 10 random movies in your Notion database.
•/help: Get a list of available commands.
'''


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not any(user.id == user_id for user in users):
        users.append(User(user_id, chat_id))

    await message.reply(
        "Hello! I'm a movie bot. Use /recommend to get a movie recommendation or /list to get random 10 movies.")


@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.reply(HELP_MSG)


@dp.message_handler(commands=['list'])
async def random_ten(message: types.Message):
    movies = notion.get_random_movies(10)
    msg = []
    for i, movie in enumerate(movies):
        msg.append(['•', movie])
    await message.reply(f"Here are 10 random movies from your list:\n\n" + tabulate(msg, tablefmt='plain'))


@dp.message_handler(commands=['recommend'])
async def recommend(message: types.Message):
    user_id = message.from_user.id
    user = next((user for user in users if user.id == user_id), None)

    if user:
        movie = notion.get_random_movies(1)
        if movie:
            await message.reply(f"Movie of the week is: \"{movie.item()}\"")
        else:
            await message.reply("There no movie left")
    else:
        await message.reply("Please use /start command first")


async def on_startup(dp):
    print("MovieBot started!")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
