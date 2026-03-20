from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from databases import db, db_orders
from keyboards.express_orders import express_orders_keyboard
from keyboards.notify_kb import notify_kb
from states.user_states import ust
from keyboards.menu import main_kb #menu_kb
from aiogram import F
from datetime import datetime, timedelta
from datetime import datetime
from databases import db_orders, db_express_orders
from keyboards.orders_kb import orders_keyboard
import traceback
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand
from aiogram import Bot as bot
from aiogram import Dispatcher
from functools import wraps
import time
import os
from dotenv import load_dotenv

load_dotenv()

admin_id = os.getenv("Admin_id")
my_id = os.getenv("my_id")
router = Router()

class User:
    def __init__(self):
        self.user_id = None
        self.user_name = None

users_dict = {}

def safe_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            print("Ошибка в хендлере:")
            print(traceback.format_exc())
    return wrapper

async def safe_edit(message, text, kb=None):
    try:
        return await message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            print(e)
        return message

async def safe_edit_by_id(bot, chat_id, message_id, text, kb=None):
    try:
        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            print(e)

@router.message(Command("start"))
@safe_handler
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    users_dict[user_id] = User()
    users_dict[user_id].user_id = user_id
    user = db.get_user(user_id)
    if user:
        await message.answer(f"Привет, {user[1]}", reply_markup = main_kb)
    else:
        await state.clear()
        await message.answer("Введите имя")
        await state.set_state(ust.state_check)

@router.message(ust.state_check)
@safe_handler
async def reg_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.text
    users_dict[user_id] = User()
    users_dict[user_id].user_id = user_id
    users_dict[user_id].user_name = user_name
    db.add_user(user_id, users_dict[user_id].user_name)

@router.callback_query(F.data == "just_buy")
@safe_handler
async def input_image_prompt(callback: CallbackQuery, state: FSMContext):
    msg = await safe_edit(
        callback.message,
        "Введите необходимые товары в формате:\n"
        "Товар Количество\n"
        "Товар Количество",
        main_kb
    )
    await state.update_data(menu_msg_id=msg.message_id)
    await state.set_state(ust.wait_products)
    await callback.answer()

@router.message(ust.wait_products)
@safe_handler
async def save_products(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    menu_msg_id = data["menu_msg_id"]
    lines = text.split("\n")
    delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_nm = db.get_user(user_id)
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            product = " ".join(parts[:-1])
            quantity = str(parts[-1])
            db_orders.add_order(
                user_nm[1],
                product,
                quantity,
                delivery_date,
                created_at
            )
    await message.delete()
    await safe_edit_by_id(
        message.bot,
        message.chat.id,
        menu_msg_id,
        "✅ Товары сохранены",
        main_kb
    )
    await state.clear()

@router.callback_query(F.data == "spisok")
@safe_handler
async def show_orders(callback: CallbackQuery):
    orders = db_orders.get_all_orders()
    text = "📦 Все заказы:\n\n"
    for order in orders:
        user = order[1]
        product = order[2]
        qty = order[3]
        date = order[4]
        text += f"<b>{product}</b> — <b>{qty}</b> ({user}|{date})\n"
    if len(orders) == 0:
        text = "📦 Нет заказов"
    await safe_edit(
        callback.message,
        text,
        orders_keyboard(orders)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
@safe_handler
async def buy_product(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])
    db_orders.delete_order(order_id)
    orders = db_orders.get_all_orders()
    if orders:
        text = "📦 Все заказы:\n\n"
        for order in orders:
            product = order[2]
            qty = order[3]
            user = order[1]
            date = order[4]
            text += f"<b>{product}</b> — <b>{qty}</b> ({user}|{date})\n"
    else:
        text = "✅ Всё куплено"
    await safe_edit(
        callback.message,
        text,
        orders_keyboard(orders)
    )
    await callback.answer("Удалено")


@router.callback_query(F.data == "close_orders")
@safe_handler
async def back_to(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = db.get_user(user_id)
    if user:
        await safe_edit(
            callback.message,
            f"Привет, {user[1]}",
            main_kb
        )
    await callback.answer()

@router.callback_query(F.data == "express_buy")
@safe_handler
async def add_express_buy (callback: CallbackQuery, state: FSMContext):
    msg = await safe_edit(
        callback.message,
        "Введите необходимые товары в формате:\n"
        "Товар Количество\n"
        "Товар Количество",
        main_kb
    )
    await state.update_data(menu_msg_id=msg.message_id)
    await state.set_state(ust.st2)
    await callback.answer()

@router.message(ust.st2)
@safe_handler
async def save_express_products(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    data1 = await state.get_data()
    menu_msg_id = data1["menu_msg_id"]
    lines = text.split("\n")
    delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_nm = db.get_user(user_id)
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            product = " ".join(parts[:-1])
            quantity = str(parts[-1])
            db_express_orders.add_express_order(
                user_nm[1],
                product,
                quantity,
                delivery_date,
                created_at
            )
    await message.delete()
    await safe_edit_by_id(
        message.bot,
        message.chat.id,
        menu_msg_id,
        "✅ Товары сохранены",
        main_kb
    )
    await state.clear()
    orders = db_express_orders.get_all_express_orders()
    if orders:
        text = "⚡ Экспресс заказы:\n\n"
        for order in orders:
            product = order[2]
            qty = order[3]
            user = order[1]
            text += f"<b>{product}</b> — <b>{qty}</b> ({user})\n"
        await message.bot.send_message(
            my_id,
            text,
            reply_markup=notify_kb()
        )

@router.callback_query(F.data == "express_spisok")
@safe_handler
async def show_express_orders(callback: CallbackQuery):
    orders = db_express_orders.get_all_express_orders()
    text = "📦 Срочные заказы:\n\n"
    for order in orders:
        user = order[1]
        product = order[2]
        qty = order[3]
        date = order[4]
        text += f"<b>{product}</b> — <b>{qty}</b> ({user}|{date})\n"
    if len(orders) == 0:
        text = "📦 Нет срочных заказов"
    await safe_edit(
        callback.message,
        text,
        express_orders_keyboard(orders)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("ebuy_"))
@safe_handler
async def buy_express_product(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])
    db_express_orders.delete_express_order(order_id)
    orders = db_express_orders.get_all_express_orders()
    if orders:
        text = "⚡ Срочные заказы:\n\n"
        for order in orders:
            product = order[2]
            qty = order[3]
            user = order[1]
            date = order[4]
            text += f"<b>{product}</b> — <b>{qty}</b> ({user}|{date})\n"
    else:
        text = "✅ Всё куплено"
    await safe_edit(
        callback.message,
        text,
        express_orders_keyboard(orders)
    )
    await callback.answer("Удалено")

@router.callback_query(F.data == "close_express_orders")
@safe_handler
async def back_to_ex(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = db.get_user(user_id)
    if user:
        await safe_edit(
            callback.message,
            f"Привет, {user[1]}",
            main_kb
        )
    await callback.answer()

@router.callback_query(F.data == "cls")
@safe_handler
async def cls(callback: CallbackQuery):
    await callback.message.delete()

@router.callback_query(F.data == "close_notify")
@safe_handler
async def close_notify(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

