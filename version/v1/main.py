import searcher_num

from loguru import logger
import datetime

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# AIOGRAM
BOT_TOKEN = "7543810363:AAGh0kKfmn1vfARHG0nWIcBI48KcfavTTFw"
ADMIN = [1020432840, 7920765657]
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


# Обработка Старта Бота
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
	logger.info('Command Start')
	# INLINE
	inline_btn_cdl = InlineKeyboardButton(text='Подобрать ГРЗ', callback_data="btn_cdl")
	inline_btn_contact = InlineKeyboardButton(text='Связаться с продавцом', url="https://t.me/NomerOK_64")
	inline_btn_group = InlineKeyboardButton(text='Telegram-канал', url="https://t.me/NomerOK64")
	inline_kb = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_cdl],[inline_btn_contact,inline_btn_group]])

	await message.answer(
		f"Привет, {message.from_user.full_name}! \nМы команда <b>НомерОк 64</b>, и мы готовы найти для тебя <b><i>красивый</i></b> авто номер(ГРЗ)!",
		reply_markup=inline_kb)

# Редактирование цены
@dp.message(Command(commands='edit'))
async def command_edit_handler(message: types.Message) -> None:
	# Изменение цены
	if int(message.from_user.id) in ADMIN:
		search_item = message.text.split()
		if len(search_item) != 3:
			logger.warning('Ошибка для команды "/edit" - ' + str(message.text) + "\nНе достаточно данных")
			await message.answer('Недостаточно данных\n\n Напоминаем. "/edit [н000нн] [цена]"')
		else:
			get_item, get_index_item = searcher_num.search_cdl(search_item[1].lower())
			if len(get_item) == 0:
				logger.warning('Ошибка для команды "/edit" - ' + str(message.text) + "\nНе найдено нужного лота")
				await message.answer('Ничего не найдено!')
			else:
				if searcher_num.edit_sdl(get_index_item[0], search_item[2]):
					logger.success('Номер "' + str(message.text) + '" успешно изменён')
					await message.answer('Номер успешно изменён!')
				else:
					logger.error('Ошибка для команды "/edit" - ' + str(message.text) + '\nНеизвестная ошибка')
					await message.answer('Неизвестная ошибка!')

# Удаление лота
@dp.message(Command(commands='delete'))
async def command_edit_handler(message: types.Message) -> None:
	# Удаление лота
	if int(message.from_user.id) in ADMIN:
		search_item = message.text.split()
		if len(search_item) != 2:
			logger.warning('Ошибка для команды "/delete" - ' + str(message.text) + "\nНе достаточно данных")
			await message.answer('Недостаточно данных\n\n Напоминаем. "/delete [н000нн]"')
		else:
			get_item, get_index_item = searcher_num.search_cdl(search_item[1].lower())
			if len(get_item) == 0:
				logger.warning('Ошибка для команды "/delete" - ' + str(message.text) + "\nНе найдено нужного лота")
				await message.answer('Ничего не найдено!')
			else:
				if searcher_num.delete_sdl(get_index_item[0]):
					logger.success('Номер "' + str(message.text) + '" успешно удалён')
					await message.answer('Номер успешно удалён!')
				else:
					logger.error('Ошибка для команды "/delete" - ' + str(message.text) + '\nНеизвестная ошибка')
					await message.answer('Неизвестная ошибка!')

# Добавление лота
@dp.message(Command(commands='add'))
async def command_edit_handler(message: types.Message) -> None:
	# Добавление лота
	if int(message.from_user.id) in ADMIN:
		search_item = message.text.split()
		if len(search_item) != 5:
			logger.warning('Ошибка для команды "/add" - ' + str(message.text) + "\nНе достаточно данных")
			await message.answer('Недостаточно данных\n\n Напоминаем. "/add [н000нн] [регион] [цена] [ключ/нет]"')
		else:
			set_key = False
			if search_item[4].lower() == "ключ" or search_item[4].lower() == "подключ" or search_item[4].lower() == "да":
				set_key = True
			new_lot = {
				"text":str(search_item[1]).lower(),
				"region":int(search_item[2]),
				"price":str(search_item[3]),
				"key":set_key
			}
			if searcher_num.add_sdl(new_lot):
				logger.success('Номер "' + str(message.text) + '" успешно добавлен')
				await message.answer('Номер успешно добавлен!')
			else:
				logger.error('Ошибка для команды "/add" - ' + str(message.text) + '\nНеизвестная ошибка')
				await message.answer('Неизвестная ошибка!')


# GET CDL
@dp.callback_query(F.data == 'btn_cdl')
async def inline_get_cdl(call: CallbackQuery):
	logger.info('Нажата кнопка "btn_cdl"')
	await bot.send_message(call.from_user.id, 
		text="Отлично, давай подберём тебе крутой номер на машину!\n\nОтправь мне буквы или цифры а остальное закрой звёздочкой(*)")
	await bot.send_photo(
		chat_id=call.from_user.id,
		photo=FSInputFile(path='src\\cdl_photo.png'))

# Обработка номера и поиск
@dp.message()
async def search_in_message(message: types.Message):
	logger.info("Введён запрос - "+str(message.text))

	# Проверка на ГРЗ
	if message.text is not None:
		if len(message.text) == 6:
			res_cdl_search_list = []
			res_cdl_search_list_index = []
			text_to_response_cdl = ""
			res_cdl_search_list, res_cdl_search_list_index = searcher_num.search_cdl(message.text.lower())

			if len(res_cdl_search_list) != 0:
				for item in res_cdl_search_list:
					text_to_response_cdl += " - <b>" + item['text'].upper() + " " + str(item['region']) + "</b>"+str(item['key'])+"  = <i>" + str(item['price']) + "</i>\n"	
			
				inline_btn_contact = InlineKeyboardButton(text='Связаться с продавцом', 
					url="https://t.me/NomerOK_64")
				inline_kb = InlineKeyboardMarkup(
					inline_keyboard=[[inline_btn_contact]])
				logger.success('По слову "'+str(message.text)+'" нашлись результаты:'+str(res_cdl_search_list))
				await bot.send_message(
					message.from_user.id,
					text="Отлично! Вот что мы нашли:\n\n"+text_to_response_cdl, reply_markup=inline_kb)

			else:
				logger.warning('Запрос с текстом "'+str(message.text)+'" ничего не выдал')
				await bot.send_message(
					message.from_user.id,
					text="Ничего не нашли. Попробуйте поменять запрос")
		else:
			logger.warning('Вводный текст "'+str(message.text)+'" превысил 6 символов')

	# Обработка Таблиц Баз Данных
	elif message.document is not None:
		if int(message.from_user.id) in ADMIN:
			logger.info("Отправления база данных")

			file = await bot.get_file(message.document.file_id)
			file_path = file.file_path

			path = 'database.xlsx'
			
			await bot.download_file(file_path, path)
			await bot.download_file(file_path, 'C:\\Users\\l_mis\\Desktop\\DEVELOP\\TG_BOT_NomerOk\\backup\\' + str(datetime.datetime.now().timestamp()) + ".xlsx")
			
			if searcher_num.xlsx_to_json():
				logger.success("База успешно обновленна")
				await message.answer('Всё прошло успешно, База обновлена!')
			else:
				logger.error("Ошибка при обработке базы")
				await message.answer('Произошла ошибка')

async def main() -> None:
	# Запускаем получение обновлений
	try:
		await dp.start_polling(bot)
	except Exception:
		logger.error(Exception)

if __name__ == "__main__":
	asyncio.run(main())