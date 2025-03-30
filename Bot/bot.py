import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand


load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

async def setup_bot_commands(bot: Bot) -> None:
    bot_commands = [
        BotCommand(command="start", description="Запустить бота"),
    ]
    await bot.set_my_commands(bot_commands)