import asyncio
from aiogram.types import BotCommand
from loader import bot, dp
from handlers import start
from utils.scheduler import start_scheduler
from utils.express_notify import express_notify
import asyncio

async def main():
    dp.include_router(start.router)
    await bot.set_my_commands([
        BotCommand(command="start", description="Старт")
    ])
    start_scheduler(bot)
    asyncio.create_task(express_notify(bot))
    await dp.start_polling(
        bot,
        polling_timeout=30
    )
#aaaaaaaa blyat
if __name__ == "__main__":
    asyncio.run(main())