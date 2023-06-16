import main
import settings

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TG_TOKEN = settings.TOKEN

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

StartButton = KeyboardButton("/help")
Normal_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(StartButton)


@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Это бот для конвертации текста в голосовое сообщение.\nНажмите на кнопку для того чтобы узнать как пользоваться ботом\nАвтор: @hkk89",
        reply_markup=Normal_kb
    )


@dp.message_handler(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply(
        "Для того чтобы бот распознал текст:\n🔸 Сообщение должно содержать менее 500 букв.\n🔸 Сообщение не должно содержать математических символов.\n🔸 Бот может не принять сообщение, это ошибка не бота, а используемой нейронной сети.\n🔸 Напишите сообщение боту и ждите."
    )


@dp.message_handler(content_types='text')
async def MainButton(message: types.Message):
    await message.reply("Текст получен")

    main.text_to_speech(message.text)

    voice = types.InputFile('speech.wav')
    await bot.send_voice(message.from_user.id, voice, caption="Ответ от бота")


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
