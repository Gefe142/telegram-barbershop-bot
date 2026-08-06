import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

import keyboards as kb
from states import Registration

ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

user = Router()

@user.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        "Hello! Welcome to the bot.\n\nEnter your name:", 
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.name)

@user.message(Registration.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Send your phone number using the button below:", reply_markup=kb.get_phone)
    await state.set_state(Registration.phone)

@user.message(Registration.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone=phone_number)

    await message.answer("Thank you for registering! Now select an action from the menu:", reply_markup=kb.menu)
    await state.clear()

@user.message(F.text == "Catalog")
async def show_catalog(message: Message, state: FSMContext):
    await message.answer("Select a service from the catalog.:", reply_markup=kb.catalog_inline)
    await state.set_state(Registration.service)

@user.message(F.text == "Contacts")
async def show_contacts(message: Message):
    await message.answer("Please write down your address, 1\nPhone: +000000000000")

@user.callback_query(Registration.service, F.data.startswith("service_"))
async def process_service_choice(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    services_map = {
        "service_haircut": "Haircut",
        "service_beard": "Beard",
        "service_combo": "Haircut + Beard"
    }
    selected_service = services_map.get(callback.data, "Послуга")
    await state.update_data(service=selected_service)
    
    await state.set_state(Registration.time)
    await callback.message.edit_text(
        f"You couse: **{selected_service}**\nNow choose a convenient time for your appointment (09:00 - 20:00):",
        reply_markup=kb.get_time_keyboard(),
        parse_mode="Markdown"
    )

@user.callback_query(Registration.time, F.data.startswith("time_"))
async def process_time_choice(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    selected_time = callback.data.split("_")[1]
    await state.update_data(time=selected_time)
    
    data = await state.get_data()
    user_name = data.get("name", callback.from_user.full_name)
    user_phone = data.get("phone", "Не вказано")
    service = data.get("service")
    
    admin_text = (
        f"🔔 **NEW APPOINTMENT!**\n\n"
        f"👤 **Client:** {user_name}\n"
        f"📞 **Phone:** {user_phone}\n"
        f"✂️ **Servise:** {service}\n"
        f"⏰ **Time:** {selected_time}\n"
        f"💬 **Telegram:** @{callback.from_user.username or 'none'}"
    )
    
    if ADMIN_ID:
        try:
            await callback.message.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending message to the administrator: {e}")

    await callback.message.edit_text(
        f"The record has been successfully created!\n\n"
        f"Servise: {service}\n"
        f"Time: {selected_time}\n\n"
        f"Thank you! We look forward to seeing you.",
        parse_mode="Markdown"
    )
    await state.clear()
