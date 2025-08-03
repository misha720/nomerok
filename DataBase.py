# Импорт
import json
import openpyxl
import pandas as pd
import os
import datetime

'''
        Класс базы данных
'''



class DataBase:
    def __init__(self, logger):

        self.logger = logger

        if os.path.isfile("data.json"):
            self.base = json.load(open("data.json"))
            self.logger.success('База данных загружена')
        else:
            # Файл базы данных не найден
            self.logger.error('Файл базы данных был повреждён.')
            # Восстановления базы
            self.base = {
                "users":[],
                "cdl":[]
            }

        self.base_cdl = self.base['cdl']
        self.base_users = self.base['users']
        # self.base_phone = self.base['phone']

    def save_base(self):
        # Сохранение базы данных в файл

        # Загрузка данных в общую переменную self.base
        self.base['cdl'] = self.base_cdl
        #self.base['sdl'] = self.base_phone
        self.base['users'] = self.base_users

        # Сохранение в файл
        with open("data.json", "w") as base_file:
            json.dump(self.base, base_file)

        self.logger.info('База данных сохранена')

        return

    def disconnect(self):
        # Отключение базы данных
        self.save_base()

        self.logger.info('База данных отключена')
        return



    #   C D L
    def get_sdl_procent_filter(self, bundle):
        bundle_dict_sorted = []
        result = []

        # Cортировка списка
        bundle_dict = dict(sorted(bundle.items(),reverse=True, key=lambda item: item[1]))
        for lot in bundle_dict:
            #print(lot)
            bundle_dict_sorted.append(lot)

        # Подтягиваем весь лот по его тексту
        for text_for_bundle in bundle_dict_sorted:
            for lot_sdl in self.base_cdl:

                if text_for_bundle == lot_sdl['text']:
                    #print(text_for_bundle)
                    # Нашлось совпадение с списком всех SDL
                    result.append(lot_sdl)


        return result

    def get_sdl(self, text):
        # Поиск по базе данных по тексту
        # Возвращает список номеров

        #   Переменные
        results = [] # Список SDL номеров для return
        array_text = list(str(text).lower()) # Текст представленный в виде массива
        procent_lot = 0  # Процент совпадения лота к тексту
        procent_offset = round(100 / len(array_text)-1, 3)  # В случае совпадения это число прибавляется к проценту
        procent_threshol = 70 # Пороговое значение для занесения лота в results
        bundle_dict = {} # Связка текста SDL лота против процента

        #   Алгоритм
        # Перебираем базу SDL
        for lot in self.base_cdl:
            lot_search_text = str(lot['text']).lower() + str(lot["region"])
            # Перебираем текст SDL в лоте
            for lot_letter_index, lot_letter_item in enumerate(lot_search_text): # - lot['text'].lower()

                # Проверяем на совпадения
                if lot_letter_index < len(array_text):
                    if array_text[lot_letter_index] == '*' or array_text[lot_letter_index] == lot_letter_item:
                        # Если совпал, прибавляем procent_offset к procent_lot
                        procent_lot += procent_offset
                else:
                    break

            # Если процент выше procent_threshol, то добавляем в bundle_dict
            if procent_lot >= procent_threshol:
                bundle_dict[str(lot['text'])] = procent_lot
            procent_lot = 0

        # Колибровка списка с помощью self.get_sdl_procent_filter
        results = self.get_sdl_procent_filter(bundle_dict)

        # Возвращение результатов
        if len(results) != 0:
            return results
        else:
            return 0

    def sdl_update(self):
        # Получает xlsx файл
        # Обрабатыевает xlsx и превращает в базу json
        # Возвращает True/False

        # Создаём новый образ таблицы cdl
        new_base = []

        # Открываем database.xlsx для openpyxl и читаем с помощью pandas
        wookbook = openpyxl.load_workbook("database.xlsx")
        pd_data = pd.read_excel('database.xlsx')

        # Превращаем pd образ в json
        raw_json_data = json.loads(pd_data.to_json())

        # Обработка табличного json
        for index, index_item in raw_json_data['ПРОДАЕТСЯ'].items():
            index_str = str(index)
            if raw_json_data['ПРОДАЕТСЯ'][index_str] != None:
                # Подготовка данных

                # TEXT

                # Проверка на наличие стобца
                if raw_json_data['ПРОДАЕТСЯ'] is not None:
                    item_text = raw_json_data['ПРОДАЕТСЯ'][index_str].replace("\t", "")
                    item_text = item_text.replace(" ", "")
                    item_text = item_text.replace("*", "?")

                    # Превращаем из буквы "О" в 0
                    if item_text[1] == "О":
                        item_text = item_text[:1] + str(0) + item_text[1 + 1:]
                    if item_text[2] == "О":
                        item_text = item_text[:2] + str(0) + item_text[2 + 1:]
                    if item_text[3] == "О":
                        item_text = item_text[:3] + str(0) + item_text[3 + 1:]
                else:
                    # Столбец не найден
                    self.logger.error("Столбец 'Продаётся' не найден")
                    return False

                # REGION
                # Проверка на наличие стобца
                if raw_json_data['РЕГ.'] is not None:
                    if raw_json_data['РЕГ.'][index_str] is not None:
                        item_region = str(raw_json_data['РЕГ.'][index_str]).replace('.0', '')
                    else:
                        item_region = ""
                else:
                    # Столбец не найден
                    self.logger.error("Столбец 'Рег.' не найден")
                    return False

                # PRICE
                # Проверка на наличие стобца
                if raw_json_data['ЦЕНА'] is not None:
                    if raw_json_data['ЦЕНА'][index_str] == "инф скр":
                        item_price = "Информация скрыта"
                    elif raw_json_data['ЦЕНА'][index_str] == "инф у адм":
                        item_price = "Уточняйте у Администратора"
                    elif raw_json_data['ЦЕНА'][index_str] == "у админа":
                        item_price = "Уточняйте у Администратора"
                    elif raw_json_data['ЦЕНА'][index_str] == "к админу":
                        item_price = "Уточняйте у Администратора"
                    elif raw_json_data['ЦЕНА'][index_str] == "розыгрыш в рулетке":
                        item_price = "Разыгрывается в рулетке"
                    elif raw_json_data['ЦЕНА'][index_str] == "пара":
                        item_price = "Продаётся в паре"
                    elif raw_json_data['ЦЕНА'][index_str] == "догов":
                        item_price = "Договорная цена"
                    elif raw_json_data['ЦЕНА'][index_str] is None:
                        item_price = "Цена не указана"
                    else:
                        item_price = str(raw_json_data['ЦЕНА'][index_str]).replace("🔥", "") + ".000"
                else:
                    # Столбец не найден
                    self.logger.error("Столбец 'Цена' не найден")
                    return False

                # KEY
                # Проверка на наличие стобца
                if raw_json_data['УСЛОВИЕ'] is not None:
                    if raw_json_data['УСЛОВИЕ'][index_str] == " 🔑 ":
                        item_key = " 🔑 "
                    elif raw_json_data['УСЛОВИЕ'][index_str] == "НА РУКИ":
                        item_key = ""
                    elif raw_json_data['УСЛОВИЕ'][index_str] is None:
                        item_key = ""
                    elif raw_json_data['УСЛОВИЕ'][index_str] == "бронь":
                        item_key = "(забронировано)"
                    elif raw_json_data['УСЛОВИЕ'][index_str] == "торг с хозяином":
                        item_key = ""
                    else:
                        item_key = ""
                else:
                    # Столбец не найден
                    self.logger.error("Столбец 'Условие' не найден")
                    return False

                new_lot = {
                    "id":0,
                    "text": item_text,
                    "region": item_region,
                    "price": item_price,
                    "key": item_key
                }

                new_base.append(new_lot)

        # Обновляем локальную базу данных
        self.base_cdl = new_base

        # Индексация базы данных
        for index_lot_cdl, lot_cdl in enumerate(self.base_cdl):
            self.base_cdl[index_lot_cdl]['id'] = index_lot_cdl

        # Сохраняем в файл
        self.save_base()

        # Удаляем database.xlsx
        os.remove('database.xlsx')

        return True

    def get_group(self, group):
        # Функция делает выборку среди номеров по общему признаку

        result_list_cdl = [] # Cписок на вывод из функции

        if group == "identical_letters":
            # Одинаковые буквы "А***АА"
            self.logger.info("Вызвана функция identical letters")

            # Перебираем список номеров
            for lot in self.base_cdl:
                lot_text = lot["text"]
                if lot_text[0] == lot_text[4] and lot_text[4] == lot_text[5]:
                    # Если совпали 1, 5 и 6 буква
                    result_list_cdl.append(lot)

        elif group == "identical_numbers":
            # Одинаковые цифры "*777**"
            self.logger.info("Вызвана функция identical numbers")

            # Перебираем список номеров
            for lot in self.base_cdl:
                lot_text = lot["text"]
                if lot_text[1] == lot_text[2] and lot_text[2] == lot_text[3]:
                    # Если совпали 2, 3 и 4 цифра
                    result_list_cdl.append(lot)

        return result_list_cdl


    #   U S E R S
    def create_user(self, user_message):
        # Создаёт пользователя по сообщению

        today_date = datetime.datetime.today()  # Сегодняшняя дата
        str_today_date = datetime.datetime.strftime(today_date, "%d.%m.%Y")

        new_user = {
            "id": int(user_message.from_user.id),
            "status": "user",
            "history":[],# Для записи отправляемых запросов
            "date_create":str(str_today_date) # Дата создания акаунта
        }
        if user_message.from_user.first_name is not None:
            new_user['first_name'] = str(user_message.from_user.first_name)

        if user_message.from_user.username is not None:
            new_user['username'] = str(user_message.from_user.username)

        # Добавляем пользователь в список и сохраняем
        self.base_users.append(new_user)
        self.save_base()
        self.logger.success("Новый пользователь - " + str(user_message.from_user.id))

        return new_user

    def add_request(self, user, text):
        # Добавляет запрос от пользователя в его историю пользователя

        # Перебираем пользователей
        for index_user, item_user in enumerate(self.base_users):
            if user['id'] == item_user['id']:
                # Нашёлся пользователь

                # Создание лота
                new_lot = {
                    "text":text,
                    "datetime":str(datetime.datetime.now())
                }
                self.base_users[index_user]['history'].append(new_lot)

                # Сохраняемся
                self.save_base()

    def get_user(self, user_message):
        # Получение карточки пользователя
        user_id = int(user_message.from_user.id)

        # Перебор пользователей
        for item_user in self.base_users:
            if item_user['id'] == user_id:
                # Если пользователь найден
                return item_user
        else:
            # пользователь не найден
            self.logger.info("Пользователь с ID[" + str(user_id) + "] - не найден. Отправлен на регистрацию.")

            return self.create_user(user_message) # Регистрация пользователя



    #   S t a t i s t i c s
    def get_statistics(self):
        # Cобирает статистику сегодняшних новых пользователей и запрашиваемых номеров(их кол-во)
        result_count_new_user = 0 # Счётчик новых пользователей
        result_count_request = 0 # Счётчик запросов за день
        today_date = datetime.datetime.today() # Сегодняшняя дата
        str_today_date = datetime.datetime.strftime(today_date, "%d.%m.%Y") # Сегодняшняя дата преобразованная в строку для смены формата

        # Сбор данных по новым пользователям
        for item_user in self.base_users:
            # Получаем дату регистрации пользователя
            user_date_registration = datetime.datetime.strptime(item_user["date_create"], "%d.%m.%Y")

            # Если дата регистрации совпала с сегодняшней то прибавляем счётчик
            if user_date_registration == datetime.datetime.strptime(str_today_date, "%d.%m.%Y"):
                result_count_new_user+=1

        # Сбор данных о новых запросах
        for lot in self.base_users:
            if lot['history'] is not None:
                for request_from_history in lot['history']:
                    user_request_date = datetime.datetime.strptime(request_from_history["datetime"], "%Y-%m-%d %H:%M:%S.%f")

                    if user_request_date.date() == datetime.date.today():
                        result_count_request+=1

        return result_count_new_user, result_count_request


