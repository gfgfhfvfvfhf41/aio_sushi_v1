from apscheduler.schedulers.asyncio import AsyncIOScheduler
from databases import db_orders
from keyboards.notify_keyboard import notify_orders_keyboard
import os
from dotenv import load_dotenv

load_dotenv()

admin_id = os.getenv("Admin_id")
my_id = os.getenv("my_id")

scheduler = AsyncIOScheduler()

async def send_daily_orders(bot):
    orders = db_orders.get_all_orders()
    if not orders:
        text = "📦 Закупка:\n\nСегодня закупки нет"
    else:
        text = "📦 Закупка:\n\n"
        for order in orders:
            product = order[2]
            qty = order[3]
            date = order[4]
            text += f"{product} — {qty} (добавлено {date})\n"
    await bot.send_message(
        admin_id,
        text,
        reply_markup=notify_orders_keyboard(orders)
    )

def start_scheduler(bot):
    scheduler.add_job(
        send_daily_orders,
        "cron",
        hour=22,
        minute=31,
        args=[bot]
    )
    scheduler.start()