from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def express_orders_keyboard(orders):

    buttons = []

    for order in orders:
        order_id = order[0]
        product = order[2]

        buttons.append([
            InlineKeyboardButton(
                text=f"✅ Куплено: {product}",
                callback_data=f"ebuy_{order_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="☑️ Назад",
            callback_data="close_express_orders"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


