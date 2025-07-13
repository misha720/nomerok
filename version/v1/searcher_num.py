import json
import openpyxl
import pandas as pd
import os

db = json.load(open("data.json"))

def data_update():
	db = json.load(open("data.json"))

def search_cdl(text:str, list_filter:str = None):
	data_update()
	crop_data_cdl = db['data_cdl']

	list_text = list(text.lower())
	res_list = []
	res_index_list = []
	second_list = []

	for index_item, item in enumerate(crop_data_cdl):
		item_text = item['text'].lower()
		second_list.append(True)

		# перебераем слово
		for letter_index, letter_item in enumerate(item_text):

			if list_text[letter_index] != '*' and letter_item != list_text[letter_index]:
				second_list[index_item] = False
				break
			elif list_text[letter_index] != '*' and list_text[letter_index] == letter_item:
				second_list[index_item] = True

	for index_second in range(len(second_list)):
		if second_list[index_second]:
			res_index_list.append(index_second)
			res_list.append(crop_data_cdl[index_second])

	# FILTER
	if list_filter == None:
		return res_list, res_index_list

def edit_sdl(index, new_prise):
	db['data_cdl'][index]['price'] = new_prise
	with open('data.json', 'w') as file:
		json.dump(db, file)

	data_update()
	return True

def delete_sdl(index):
	list_data_cdl = list(db['data_cdl'])
	list_data_cdl.pop(index)
	db['data_cdl'] = list_data_cdl
	with open('data.json', 'w') as file:
		json.dump(db, file)

	data_update()
	return True

def add_sdl(item):
	list_data_cdl = list(db['data_cdl'])
	list_data_cdl.append(item)
	db['data_cdl'] = list_data_cdl
	with open('data.json', 'w') as file:
		json.dump(db, file)

	data_update()
	return True

def dump_new_base():
	new_base = []
	db_back = json.load(open("src\\data.json"))

	with open('src\\dump.txt','r') as file_dump:
		#print(file_dump.readlines())
		for line in file_dump.readlines():
			line.replace('\n', '')
			list_line = line.split()
			new_lot = {
				"text":list_line[0],
				"region":list_line[1],
				"price":list_line[2],
				"key":True,
			}
			new_base.append(new_lot)
		print(new_base)

	db_back['data_cdl'] = new_base
	with open('src\\data.json', 'w') as file:
		json.dump(db_back, file)

def corrector():

	db_back = json.load(open("data.json"))

	for index, item in enumerate(db_back['data_cdl']):
		if item['text'][1] == "О":
			item['text'] = item['text'][:1] + str(0) + item['text'][1+1:]
		if item['text'][2] == "О":
			item['text'] = item['text'][:2] + str(0) + item['text'][2+1:]
		if item['text'][3] == "О":
			item['text'] = item['text'][:3] + str(0) + item['text'][3+1:]

		db_back['data_cdl'][index]['text'] = item['text']

	with open('data.json', 'w') as file:
		json.dump(db_back, file)

def xlsx_to_json():
	new_base = {"data_cdl":[]}
	wookbook = openpyxl.load_workbook("database.xlsx")
	worksheet = wookbook.active

	data = pd.read_excel('database.xlsx')
	json_data = json.loads(data.to_json())

	# Обработка табличного json
	for index, index_item in json_data['ПРОДАЕТСЯ'].items():
		index_str = str(index)

		if json_data['ПРОДАЕТСЯ'][index_str] != None:
			# Подготовка данных

			# TEXT
			item_text = json_data['ПРОДАЕТСЯ'][index_str].replace("\t", "")
			item_text = item_text.replace(" ", "")

			if item_text[1] == "О":
				item_text = item_text[:1] + str(0) + item_text[1+1:]
			if item_text[2] == "О":
				item_text = item_text[:2] + str(0) + item_text[2+1:]
			if item_text[3] == "О":
				item_text = item_text[:3] + str(0) + item_text[3+1:]

			# REGION
			if json_data['РЕГ.'][index_str] is not None:
				item_region = str(json_data['РЕГ.'][index_str]).replace('.0', '')
			else:
				item_region = ""


			# PRICE
			if json_data['ЦЕНА'][index_str] == "инф скр":
				item_price = "Информация скрыта"
			elif json_data['ЦЕНА'][index_str] == "инф у адм":
				item_price = "Уточняйте у Администратора"
			elif json_data['ЦЕНА'][index_str] == "у админа":
				item_price = "Уточняйте у Администратора"
			elif json_data['ЦЕНА'][index_str] == "к админу":
				item_price = "Уточняйте у Администратора"
			elif json_data['ЦЕНА'][index_str] == "розыгрыш в рулетке":
				item_price = "Разыгрывается в рулетке"
			elif json_data['ЦЕНА'][index_str] == "пара":
				item_price = "Продаётся в паре"
			elif json_data['ЦЕНА'][index_str] == "догов":
				item_price = "Договорная цена"
			elif json_data['ЦЕНА'][index_str] == None:
				item_price = "Цена не указана"
			else:
				item_price = str(json_data['ЦЕНА'][index_str]).replace("🔥", "") + ".000"

			# KEY
			if json_data['УСЛОВИЕ'][index_str] == " 🔑 ":
				item_key = " 🔑 "
			elif json_data['УСЛОВИЕ'][index_str] == "НА РУКИ":
				item_key = ""
			elif json_data['УСЛОВИЕ'][index_str] is None:
				item_key = ""
			elif json_data['УСЛОВИЕ'][index_str] == "бронь":
				item_key = "(забронировано)"
			elif json_data['УСЛОВИЕ'][index_str] == "торг с хозяином":
				item_key = ""

			new_lot = {
				"text": item_text,
				"region": item_region,
				"price": item_price,
				"key": item_key
			}

			new_base['data_cdl'].append(new_lot)


	# Update
	os.remove('data.json')
	with open('data.json', 'w') as file:
		json.dump(new_base, file)

	corrector()

	data_update()
	return True

# if __name__ == "__main__":
# 	corrector()