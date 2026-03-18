from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = InlineKeyboardMarkup(inline_keyboard=[

    [
        InlineKeyboardButton(text="🧊 Нужно закупить", callback_data="just_buy"),
        InlineKeyboardButton(text="❗ Срочно закупить", callback_data="express_buy")
    ],

    [
        InlineKeyboardButton(text="📜 Список", callback_data="spisok"),
        InlineKeyboardButton(text="📕 Срочный список", callback_data="express_spisok")
    ],

])

# main_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="🧊 Нужно закупить", callback_data="just_buy")],
#     [InlineKeyboardButton(text="❗ Срочно закупить", callback_data="express_buy")],
#     [InlineKeyboardButton(text="📜 Список", callback_data="spisok")],
#     [InlineKeyboardButton(text="📕Срочный список", callback_data="srochiy_spisok")],
# ])

# menu_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Нужно закупить")]
#     ],
#     resize_keyboard=True
# )