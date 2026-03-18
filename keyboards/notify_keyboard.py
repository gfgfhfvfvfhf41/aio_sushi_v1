from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def notify_orders_keyboard(orders):

    buttons = []

    for order in orders:
        order_id = order[0]
        product = order[2]

        buttons.append([
            InlineKeyboardButton(
                text=f"✅ Куплено: {product}",
                callback_data=f"buy_{order_id}"
            )
        ])

    buttons.append([InlineKeyboardButton(text="❌ Закрыть", callback_data="cls")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


