from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def orders_keyboard(orders):
    buttons = []
    if orders:
        for order in orders:
            order_id = order[0]
            product = order[2]
            buttons.append([
                InlineKeyboardButton(
                    text=f"✅ Куплено: {product}",
                    callback_data=f"buy_{order_id}"
                )
            ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="🔄 Обновить",
                callback_data="refresh_orders"
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text="☑️ Назад",
            callback_data="close_orders"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)