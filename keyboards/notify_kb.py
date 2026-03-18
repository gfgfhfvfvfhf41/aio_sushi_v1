from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def notify_kb():

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Закрыть",
                    callback_data="close_notify"
                )
            ]
        ]
    )

    return kb