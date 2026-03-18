# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from datetime import datetime
# from databases import db_orders
# from keyboards.orders_kb import orders_keyboard
# from keyboards.notify_keyboard import notify_orders_keyboard
#
# scheduler = AsyncIOScheduler()
#
# async def send_daily_orders(bot):
#     today = datetime.now().strftime("%Y-%m-%d")
#     orders = db_orders.get_all_orders()
#     text = "📦 Закупка:\n\n"
#     for order in orders:
#         product = order[2]
#         qty = order[3]
#         text += f"{product} — {qty}\n"
#     if len(orders) == 0:
#         text = "📦 Сегодня закупки нет"
#     # ID куда отправлять
#     chat_id = 905618101  #762138557 #1649502024
#     await bot.send_message(
#         chat_id,
#         text,
#         reply_markup=notify_orders_keyboard(orders)
#     )
# def start_scheduler(bot):
#     scheduler.add_job(
#         send_daily_orders,
#         "cron",
#         hour=5,
#         minute=30,
#         args=[bot]
#     )
#     scheduler.start()



from apscheduler.schedulers.asyncio import AsyncIOScheduler
from databases import db_orders
from keyboards.notify_keyboard import notify_orders_keyboard

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
        905618101,
        text,
        reply_markup=notify_orders_keyboard(orders)
    )
    #762138557

def start_scheduler(bot):
    scheduler.add_job(
        send_daily_orders,
        "cron",
        hour=5,
        minute=30,
        args=[bot]
    )
    scheduler.start()