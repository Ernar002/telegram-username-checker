import asyncio
from telethon import TelegramClient, errors
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Вставь свои данные
BOT_TOKEN = "YOU_BOT_TOKEN"
API_ID = "YOU_API_ID"
API_HASH = "YOU_API_HASH"

# Инициализация бота и клиента Telethon
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = TelegramClient('checker', API_ID, API_HASH)

# Функция проверки username
async def check_username(username):
    try:
        await client.get_entity(username)
        return f"❌ Username @{username} занят."
    except errors.UsernameInvalidError:
        return f"⚠️ Некорректный формат username: @{username}"
    except ValueError:
        return f"✅ Username @{username} доступен!"
    except errors.RPCError as e:
        return f"⚠️ Ошибка при проверке @{username}: {e}"

# Обработка команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("👋 Привет! Отправь мне username для проверки.")

# Обработка сообщений с username
@dp.message()
async def handle_message(message: Message):
    usernames = message.text.split()
    if not usernames:
        await message.answer("❌ Пожалуйста, отправьте хотя бы один username.")
        return

    results = []
    async with client:
        for username in usernames:
            username = username.lstrip("@")
            result = await check_username(username)
            results.append(result)

    await message.answer("\n".join(results))

# Запуск клиента и бота
async def main():
    print("Бот запущен!")
    await client.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
