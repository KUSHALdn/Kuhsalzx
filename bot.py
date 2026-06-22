import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIGURATION ---
# IMPORTANT: BotFather se naya token lekar yahan daalein
BOT_TOKEN = "8878551213:AAEuXkfq8ZLkBZYZ7umIhrePCWKyinJObDw" 
MONGO_URI = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority"

# Initialization
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db_client = AsyncIOMotorClient(MONGO_URI)
db = db_client['kushal_bot']

# CC Result Formatter (Design)
def get_cc_design(cc, status, response, bank, country, gateway, user_name, user_id):
    return (
        f"━━━━━━━━━━━━━━\n"
        f"💳 **CC:** `{cc}`\n"
        f"📡 **Status:** {status}\n"
        f"📝 **Response:** {response}\n"
        f"━━━━━━━━━━━━━━\n"
        f"🏦 **Bank:** {bank}\n"
        f"🌍 **Country:** {country}\n"
        f"🛠 **Gateway:** {gateway}\n"
        f"━━━━━━━━━━━━━\n"
        f"👤 **Checked by:** {user_name}\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"━━━━━━━━━━━━━━"
    )

# Logic to handle /check command
@dp.message(F.text.startswith("/check"))
async def handle_check(message: types.Message):
    # User ka data nikalna
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    
    # CC number nikalna (command ke baad wala text)
    args = message.text.split()
    if len(args) < 2:
        await message.reply("Format: `/check 4242424242424242`")
        return
    
    cc_number = args[1]
    
    # Yahan tumhara Gateway Logic ayega
    # Filhardhaal default status display
    response_msg = get_cc_design(
        cc=cc_number,
        status="Maintenance 🛠",
        response="Gate under maintenance (Invalid SK). Please contact Admin.",
        bank="Stripe Payments Uk Limited",
        country="United Kingdom 🇬🇧",
        gateway="Stripe",
        user_name=user_name,
        user_id=user_id
    )
    
    await message.answer(response_msg, parse_mode="Markdown")

async def main():
    print("Bot is ready and running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
