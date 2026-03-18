from aiogram import types
from loader import dp, bot

keyboard_for_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
buy_game = types.KeyboardButton("")
wallet = types.KeyboardButton("")
keyboard_for_menu.add()