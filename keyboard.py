from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Catalog")],
        [KeyboardButton(text="Contacts")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Select a menu item"
)

get_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send phone number", request_contact=True)],
    ],
    resize_keyboard=True
)

catalog_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Haircut", callback_data="service_haircut")],
        [InlineKeyboardButton(text="Beard", callback_data="service_beard")],
        [InlineKeyboardButton(text="Haircut + Beard", callback_data="service_combo")]
    ]
)

def get_time_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for hour in range(9, 21):
        time_str = f"{hour:02d}:00"
        buttons.append(
            InlineKeyboardButton(text=time_str, callback_data=f"time_{time_str}")
        )
    
    keyboard = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
