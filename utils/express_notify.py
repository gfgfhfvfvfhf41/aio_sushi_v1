# import asyncio
# from databases import db_express_orders
# from keyboards.notify_kb import notify_kb
#
# ADMIN_ID = 905618101 #762138557
#
#
# async def express_notify(bot):
#
#     while True:
#
#         orders = db_express_orders.get_all_express_orders()
#
#         if orders:
#
#             text = "⚡ Экспресс заказы:\n\n"
#
#             for order in orders:
#                 product = order[2]
#                 qty = order[3]
#                 user = order[1]
#
#                 text += f"{product} — {qty} ({user})\n"
#
#             await bot.send_message(
#                 ADMIN_ID,
#                 text,
#                 reply_markup=notify_kb()
#             )
#
#         await asyncio.sleep(3600)  # каждый час 3600
import asyncio
from databases import db_express_orders
from keyboards.notify_kb import notify_kb


async def express_notify(bot):
    while True:
        try:
            orders = db_express_orders.get_all_express_orders()
            if orders:
                text = "⚡ Экспресс заказы:\n\n"
                for order in orders:
                    product = order[2]
                    qty = order[3]
                    user = order[1]
                    text += f"{product} — {qty} ({user})\n"
                await bot.send_message(
                    905618101,
                    text,
                    reply_markup=notify_kb()
                )
                #762138557
        except Exception as e:
            print("EXPRESS ERROR:", e)
        await asyncio.sleep(3600)