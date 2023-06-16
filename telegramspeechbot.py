import main
import settings

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

TG_TOKEN = settings.TOKEN

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

StartButton = KeyboardButton("/help")
SettingsButton = KeyboardButton("/settings")
Normal_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(StartButton, SettingsButton)

Female_btn = InlineKeyboardButton('Женский', callback_data='FEMALE')
Male_btn = InlineKeyboardButton('Мужской', callback_data='MALE')
inline_kb1 = InlineKeyboardMarkup().add(Female_btn, Male_btn)

Anna_btn = InlineKeyboardButton('Анна Кравчук', callback_data="ru-RU_Anna Kravchuk")
Natalya_btn = InlineKeyboardButton('Наталия Сучова', callback_data="ru-RU_Natalia Sychyov")
FemaleSpeaker_kb = InlineKeyboardMarkup().add(Anna_btn, Natalya_btn)

Alex_btn = InlineKeyboardButton('Алексей Сёмин', callback_data="ru-RU_Alexei Syomi")
Ivan_btn = InlineKeyboardButton('Иван Чкалов', callback_data="ru-RU_Ivan Chkalov")
MaleSpeaker_kb = InlineKeyboardMarkup().add(Alex_btn, Ivan_btn)


@dp.message_handler(commands=['settings'])
async def process_command_1(message: types.Message):
    await message.reply(text="Выберите пол спикера:", reply_markup=inline_kb1)


@dp.callback_query_handler(text=["FEMALE", "MALE"])
async def process_command_2(callback: CallbackQuery):
    if callback.data == Female_btn.callback_data:
        settings.Sex = f"{Female_btn.callback_data}"
        await callback.message.edit_text(text="Выберите чей голос использовать:", reply_markup=FemaleSpeaker_kb)
    elif callback.data == Male_btn.callback_data:
        settings.Sex = f"{Male_btn.callback_data}"
        await callback.message.edit_text(text="Выберите чей голос использовать:", reply_markup=MaleSpeaker_kb)


@dp.callback_query_handler(text=["ru-RU_Anna Kravchuk", "ru-RU_Natalia Sychyov", "ru-RU_Alexei Syomi", "ru-RU_Ivan Chkalov"])
async def process_command_2(callback: CallbackQuery):
    await callback.message.edit_text(text="Готово!")
    if callback.data == Anna_btn.callback_data:
        settings.Voice = f"{Anna_btn.callback_data}"
    elif callback.data == Natalya_btn.callback_data:
        settings.Voice = f"{Natalya_btn}"
    if callback.data == Alex_btn.callback_data:
        settings.Voice = f"{Alex_btn.callback_data}"
    elif callback.data == Ivan_btn.callback_data:
        settings.Voice = f"{Ivan_btn.callback_data}"


@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Это бот для конвертации текста в голосовое сообщение.\nНажмите на кнопку для того чтобы узнать как пользоваться ботом\nАвтор: @hkk89",
        reply_markup=Normal_kb
    )


@dp.message_handler(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply(
        "Для того чтобы бот распознал текст:\n🔸 Сообщение должно содержать менее 500 букв.\n🔸 Сообщение не должно содержать математических символов.\n🔸 Бот может не принять сообщение, это ошибка не бота, а используемой нейронной сети.\n🔸 Напишите сообщение боту и ждите.\n🔸 Для настройки голоса бота нажмите вторую кнопку"
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
