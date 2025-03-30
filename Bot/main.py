from ChapterChecker import client
from bot import dp, bot, setup_bot_commands
from handler import router
import asyncio


async def run_all():
    dp.include_router(router)
    await client.start()
    telethon_task = asyncio.create_task(client.run_until_disconnected())
    try:
        await setup_bot_commands(bot)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        print(f"Ошибка в боте: {e}")
    finally:
        await bot.session.close()
        telethon_task.cancel()


if __name__ == '__main__':
    asyncio.run(run_all())