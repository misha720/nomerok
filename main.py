import json

#import searcher_num
from DataBase import DataBase

from loguru import logger
import datetime

from contextlib import suppress

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

# AIOGRAM
BOT_TOKEN = "7543810363:AAGh0kKfmn1vfARHG0nWIcBI48KcfavTTFw"
ADMIN = [1020432840] # Список админов
WORK_CHAT = [1002558393642] # Список рабочих чатов, где бот модератор
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# Data Base
base = DataBase(logger)

#	Переменные
forbidden_words = ["казино","зарабатывать","подработка","usdt","вложения","схема","задание","платим","халтурка"]

# Обработка Старта Бота
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    # Ограницения для работы только в личных сообщениях
    if message.chat.type == 'private':

        logger.info('Command Start')

        # Ищем пользователя в базе
        base.get_user(message)
        # INLINE
        inline_btn_cdl = InlineKeyboardButton(text='Подобрать ГРЗ', callback_data="btn_cdl")
        inline_btn_contact = InlineKeyboardButton(text='Связаться с продавцом', url="https://t.me/NomerOK_64")
        inline_btn_group = InlineKeyboardButton(text='Telegram-канал', url="https://t.me/NomerOK64")
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_cdl],[inline_btn_contact,inline_btn_group]])

        await message.answer(
            f"Привет, {message.from_user.full_name}! \nМы команда <b>НомерОк 64</b>, и мы готовы найти для тебя <b><i>красивый</i></b> авто номер(ГРЗ)!",
            reply_markup=inline_kb)

# Кнопка identical_letters
@dp.callback_query(F.data == 'identical_letters')
async def identical_letters(call: CallbackQuery):
    text_to_response_cdl = "Отлично! Вот что мы нашли:\n\n"  # Сообщеине с SDL лотами для вывода
    sdl_list = base.get_group("identical_letters")  # Отправка текста на поиск SDL списка

    logger.debug(sdl_list)

    # Если sdl_list не пустой
    if sdl_list != 0:

        # Инлайн клавиатура
        inline_btn_contact = InlineKeyboardButton(text='Связаться с продавцом',
                                                  url="https://t.me/NomerOK_64")
        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[[inline_btn_contact]])

        # Защита от длинных сообщений
        index_position_for_sdl = 0
        if len(sdl_list) > 72:
            for lot in sdl_list:
                if index_position_for_sdl <= 72:
                    index_position_for_sdl += 1
                    text_to_response_cdl += " - <b>" + lot['text'].upper() + " " + str(lot['region']) + "</b>" + str(
                        lot['key']) + "  = <i>" + str(lot['price']) + "</i>\n"
                else:
                    # Отправка сообщения пользователю
                    logger.debug("Enter text")
                    await bot.send_message(
                        call.from_user.id,
                        text=text_to_response_cdl, reply_markup=inline_kb)

                    index_position_for_sdl = 0
                    text_to_response_cdl = ""
        else:
            for lot in sdl_list:
                text_to_response_cdl += " - <b>" + lot['text'].upper() + " " + str(lot['region']) + "</b>" + str(
                    lot['key']) + "  = <i>" + str(lot['price']) + "</i>\n"

            # Отправка сообщения пользователю
            await bot.send_message(
                call.from_user.id,
                text=text_to_response_cdl, reply_markup=inline_kb)

# Кнопка identical_numbers
@dp.callback_query(F.data == 'identical_numbers')
async def identical_numbers(call: CallbackQuery):
    text_to_response_cdl = "Отлично! Вот что мы нашли:\n\n"  # Сообщеине с SDL лотами для вывода
    sdl_list = base.get_group("identical_numbers")  # Отправка текста на поиск SDL списка

    logger.debug(sdl_list)

    # Если sdl_list не пустой
    if sdl_list != 0:

        # Инлайн клавиатура
        inline_btn_contact = InlineKeyboardButton(text='Связаться с продавцом',
                                                  url="https://t.me/NomerOK_64")
        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[[inline_btn_contact]])

        # Защита от длинных сообщений
        index_position_for_sdl = 0
        if len(sdl_list) > 72:
            for lot in sdl_list:
                if index_position_for_sdl <= 72:
                    index_position_for_sdl += 1
                    text_to_response_cdl += " - <b>" + lot['text'].upper() + " " + str(lot['region']) + "</b>" + str(
                        lot['key']) + "  = <i>" + str(lot['price']) + "</i>\n"
                else:
                    # Отправка сообщения пользователю
                    logger.debug("Enter text")
                    await bot.send_message(
                        call.from_user.id,
                        text=text_to_response_cdl, reply_markup=inline_kb)

                    index_position_for_sdl = 0
                    text_to_response_cdl = ""
        else:
            for lot in sdl_list:
                text_to_response_cdl += " - <b>" + lot['text'].upper() + " " + str(lot['region']) + "</b>" + str(
                    lot['key']) + "  = <i>" + str(lot['price']) + "</i>\n"

            # Отправка сообщения пользователю
            await bot.send_message(
                call.from_user.id,
                text=text_to_response_cdl, reply_markup=inline_kb)

# Кнопка "GET CDL"
@dp.callback_query(F.data == 'btn_cdl')
async def inline_get_cdl(call: CallbackQuery):
    # Ограницения для работы только в личных сообщениях
    if call.message.chat.type == 'private':

        logger.info('Нажата кнопка "btn_cdl"')

        # INLINE
        inline_identical_letters = InlineKeyboardButton(text='Одинаковые буквы', callback_data="identical_letters")
        inline_identical_numbers = InlineKeyboardButton(text='Одинаковые цифры', callback_data="identical_numbers")
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[[inline_identical_letters],[inline_identical_numbers]])

        await bot.send_message(call.from_user.id,
            text="Отлично, давай подберём тебе крутой номер на машину!\n\nОтправь мне буквы или цифры а остальное закрой звёздочкой(*)",
            reply_markup=inline_kb)
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=FSInputFile(path='src\\cdl_photo.png'))

# Кнопка "Заблокировать"
@dp.callback_query(F.data == 'blok_user')
async def inline_get_cdl(call: CallbackQuery):
    text_call = call.message.text.split()

    user_for_baned = text_call[5]
    # Блокировка
    with suppress(TelegramBadRequest):
        print(await bot.ban_chat_member(chat_id=WORK_CHAT[0], user_id=int(user_for_baned)))

# Обработка команды /statistics
@dp.message(F.text == "/statistics")
async def get_statistics(message: types.Message):
    if int(message.from_user.id) in ADMIN:
        # Отправляем запрос на подготовку данных
        count_new_user, count_request = base.get_statistics()

        # Форматируем текст
        today_date = datetime.datetime.today()  # Сегодняшняя дата
        str_today_date = datetime.datetime.strftime(today_date,"%d.%m.%Y")  # Сегодняшняя дата преобразованная в строку для смены формата

        text_for_answer = "Статистика на сегодняшний день: <b><i>" + str_today_date + "</i></b>\n\n\t\t\t\t<b>Новых пользователей</b> - " + str(count_new_user) + "\n\t\t\t\t<b>Запросов сделано</b> - " + str(count_request)

        # Отправка сообщения в чат
        await message.answer(text_for_answer)

# Обработка номера и поиск
@dp.message()
async def search_in_message(message: types.Message):

    # Ограницения для работы только в личных сообщениях
    if message.chat.type == 'private':

        logger.info("Введён запрос - "+str(message.text))
        # Добавление запроса в историю пользователя
        user = base.get_user(message)
        base.add_request(user=user, text=message.text)

        # Проверка на ГРЗ
        if message.text is not None:
            #if len(message.text) == 6:
                text_to_response_cdl = "Отлично! Вот что мы нашли:\n\n" # Сообщеине с SDL лотами для вывода
                sdl_list = base.get_sdl(message.text) # Отправка текста на поиск SDL списка

                # Если sdl_list не пустой
                if sdl_list != 0:

                    # Инлайн клавиатура
                    inline_btn_contact = InlineKeyboardButton(text='Связаться с продавцом',
                                                              url="https://t.me/NomerOK_64")
                    inline_kb = InlineKeyboardMarkup(
                        inline_keyboard=[[inline_btn_contact]])

                    # Вывод сообщения в терминал
                    logger.success('По слову "' + str(message.text) + '" нашлись результаты:' + str(sdl_list))

                    # Защита от длинных сообщений
                    index_position_for_sdl = 0
                    if len(sdl_list) > 72:
                        for lot in sdl_list:
                            if index_position_for_sdl <= 72:
                                index_position_for_sdl += 1
                                text_to_response_cdl += " - <b>" + lot['text'].upper() + " " + str(lot['region']) + "</b>" + str(lot['key']) + "  = <i>" + str(lot['price']) + "</i>\n"
                            else:
                                # Отправка сообщения пользователю
                                await bot.send_message(
                                    message.from_user.id,
                                    text=text_to_response_cdl, reply_markup=inline_kb)

                                index_position_for_sdl = 0
                                text_to_response_cdl = ""
                    else:
                        for lot in sdl_list:
                            text_to_response_cdl += " - <b>" + lot['text'].upper() + " " + str(
                                lot['region']) + "</b>" + str(
                                lot['key']) + "  = <i>" + str(lot['price']) + "</i>\n"

                        # Отправка сообщения пользователю
                        await bot.send_message(
                            message.from_user.id,
                            text=text_to_response_cdl, reply_markup=inline_kb)


                # Если sdl_list пустой
                else:
                    logger.warning('Запрос с текстом "'+str(message.text)+'" ничего не выдал')
                    await bot.send_message(
                        message.from_user.id,
                        text="Ничего не нашли. Попробуйте поменять запрос")
            #else:
            #    logger.warning('Вводный текст "'+str(message.text)+'" превысил 6 символов')

        # Обработка Таблиц Баз Данных
        elif message.document is not None:
            if int(message.from_user.id) in ADMIN:
                logger.info("Получена база данных")

                # Получаем файл по айди
                received_file = await bot.get_file(message.document.file_id)
                file_path = received_file.file_path

                # Название файла
                path = 'database.xlsx'

                # Скачиваем файл
                await bot.download_file(file_path, path)
                # Делаем бэкап базы номеров
                await bot.download_file(file_path, 'C:\\Users\\l_mis\\Desktop\\DEVELOP\\TG_BOT_NomerOk\\backup\\' + str(datetime.datetime.now().timestamp()) + ".xlsx")

                # Запускаем обработку базы данных
                if base.sdl_update():
                    # Если установка прошла успешно
                    logger.success("База успешно обновленна")
                    await message.answer('Всё прошло успешно, База обновлена!')
                else:
                    # Возникла ошибка при обработке базы
                    logger.error("Ошибка при обработке базы")
                    await message.answer('Произошла ошибка')

    # Ограницения для работы только в чате(Модератор)
    elif message.chat.type == 'supergroup':
        # Только текст
        if message.text is not None:
            #Обработка сообщения
            user_text = str(message.text).lower().split()

            #	Проверка на запрещённые слова
            # Перебираем каждое слово
            for word_user_message in user_text:
                if word_user_message in forbidden_words:

                    # Удаление
                    with suppress(TelegramBadRequest):
                        print(await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id))

                    # Инлайн с отменой
                    inline_btn_unlock_user = InlineKeyboardButton(text='Заблокировать', callback_data="blok_user")
                    inline_kb = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_unlock_user]])
                    # Отчёт бота о блокировке
                    for admin_id in ADMIN:
                        await bot.send_message(
                            admin_id,
                            text="Заметил подозрительное сообщение от пользователя "+ str(message.from_user.id) + " с сообщением:\n\n" + str(message.text),
                            reply_markup=inline_kb)

async def main() -> None:
    # Запускаем получение обновлений
    try:
        await dp.start_polling(bot)
    except Exception:
        logger.error(Exception)

if __name__ == "__main__":
    asyncio.run(main())