import asyncio
from databases import db_express_orders
from keyboards.notify_kb import notify_kb
import os
from dotenv import load_dotenv

load_dotenv()

admin_id = os.getenv("Admin_id")
my_id = os.getenv("my_id")

last_express_message = None

async def express_notify(bot):
    global last_express_message
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
                if last_express_message:
                    try:
                        await bot.delete_message(admin_id, last_express_message)
                    except:
                        pass
                msg = await bot.send_message(
                    admin_id,
                    text,
                    reply_markup=notify_kb()
                )
                last_express_message = msg.message_id
        except Exception as e:
            print("EXPRESS ERROR:", e)
        await asyncio.sleep(21600)