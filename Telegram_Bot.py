import telebot
from config import token  # из файла config.py забираем переменную token с токеном (полученным от BotFAther)
from telebot import types  # для работы с кнопками

bot = telebot.TeleBot(token)  # создаем экземпляр бота

# Будем использовать словари, в которых будут храниться ниже указанные данные.
dict_cities = {}  # словарь, для хранения названий городов
dict_cinema = {}  # словарь, для хранения названий кинотеатров и театров
dict_halls = {}  # словарь, для хранения названий залов кинотеатров и театров


# Функция для обработки команды /start
@bot.message_handler(commands=['start'])  # команда для запуска бота
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем пользовательскую клавиатуру с встроенными
                                                              # кнопками ответа на сообщение бота.
                                                              # Если True, то размер клавиатуры будет автоматически
                                                              # именяться в зависимости от количества кнопок,
                                                              # если False, то клавиатура будет оставаться постоянной.
    markup.add('Брест', 'Гродно', 'Гомель')  # создаем кнопки и добавляем в клавиатуру
    markup.add('Витебск', 'Могилев', 'Минск')  # создаем кнопки и добавляем в клавиатуру
    bot.send_message(message.chat.id, 'Привет!')  # в телеграм бот отправляется сообщение от бота
    bot.send_message(message.chat.id, 'Выберите город', reply_markup=markup)  # + отправляется сообщение и клавиатура


# Создаем анонимную функцию (лямбда-функция), которая проверяет, содержится ли текстовое сообщение в списке. Если оно
# содержится, то будет создана клавиатура.
@bot.message_handler(func=lambda message: message.text in ['Брест', 'Гродно', 'Гомель'])
def select_city(message):
    selected_city = message.text  # переменной присваиваем значение (текстовое сообщение)
    dict_cities[message.chat.id] = selected_city  # в словаре создается запись с ключом (идентификатор чата), значением
                                                  # этого ключа будет значение переменной selected_city
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Кинотеатры', 'Театры')
    markup.add('👈 Назад к выбору города')
    bot.send_message(message.chat.id, 'Куда хотите пойти?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👈 Назад к выбору города')
def back_select_city(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Брест', 'Гродно', 'Гомель')
    markup.add('Витебск', 'Могилев', 'Минск')
    bot.send_message(message.chat.id, 'Выберите город', reply_markup=markup)


# Создаем анонимную функцию (лямбда-функция), которая проверяет, содержится ли текстовое сообщение в списке. Если оно
# содержится, то будет создана клавиатура и будут выполняться операторы ветвления.
@bot.message_handler(func=lambda message: message.text in ['Кинотеатры', 'Театры'])
def select_kino_theater(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    selected_city = dict_cities.get(message.chat.id)  # используем метод get(), происходит извлечение значения
                                                      # из словаря по ключу message.chat.id,
                                                      # и присвоение переменной selected_city.
    if message.text == 'Кинотеатры':
        if selected_city == 'Брест':
            markup.add('Кинотеатр Беларусь', 'Кинотеатр Мир')
            markup.add('👈 Назад к выбору кино и театр')
        elif selected_city == 'Гродно':
            markup.add('Кинотеатр Восток', 'К/т Красная звезда', 'Кинотеатр Октябрь', 'МЦ Гродно', 'Кинотеатр Mooon')
            markup.add('👈 Назад к выбору кино и театр')
        elif selected_city == 'Гомель':
            markup.add('Кинотеатр Мир', 'К/т им. М.И.Калинина', 'Кинотеатр Октябрь', 'Кинотеатр Misteria')
            markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите кинотеатр', reply_markup=markup)
    elif message.text == 'Театры':
        if selected_city == 'Брест':
            markup.add('Драмтеатр', 'Театр кукол')
            markup.add('👈 Назад к выбору кино и театр')
        elif selected_city == 'Гродно':
            markup.add('Драмтеатр', 'Театр кукол')
            markup.add('👈 Назад к выбору кино и театр')
        elif selected_city == 'Гомель':
            markup.add('Драмтеатр', 'Театр кукол')
            markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите театр', reply_markup=markup)
    if message.text in ['Кинотеатры', 'Театры']:
        cinema(message)  # функция cinema вызывается когда текст сообщения соответствует 'Кинотеатры' или 'Театры'.
                         # Когда приходит сообщение с текстом 'Кинотеатры' или 'Театры', функция select_kino_theater
                         # срабатывает и вызывает функцию cinema, передавая ей сообщение пользователя.
                         # С помощью этого фрагмента кода, можно связать функцию select_kino_theater и функцию cinema.


@bot.message_handler(func=lambda message: message.text == '👈 Назад к выбору кино и театр')
def back_select_kino_theater(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Кинотеатры', 'Театры')
    markup.add('👈 Назад к выбору города')
    bot.send_message(message.chat.id, 'Куда хотите пойти?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Кинотеатр Беларусь', 'Кинотеатр Мир',
                                                           'Кинотеатр Восток', 'К/т Красная звезда',
                                                           'Кинотеатр Октябрь', 'МЦ Гродно', 'Кинотеатр Mooon',
                                                           'К/т им. М.И.Калинина', 'Кинотеатр Misteria',
                                                           'Драмтеатр', 'Театр кукол'])
def select_cinema(message):
    kino_theater = message.text  # переменной присваиваем значение (текстовое сообщение)
    dict_cinema[message.chat.id] = kino_theater  # в словаре создается запись с ключом (идентификатор чата), значением
                                                 # этого ключа будет значение переменной kino_theater
    selected_city = dict_cities.get(message.chat.id)  # используем метод get(), из словаря извлекаем значение по ключу
                                                      # message.chat.id, и присваиваем переменной selected_city.
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Кинотеатр Беларусь' and selected_city == 'Брест':
        with open('D:/new/photo.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал №1(Большой)', 'Зал №2(Малый)', 'Зал №3(VIP)')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Брест, ул. Советская, 62')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'Кинотеатр Мир' and selected_city == 'Брест':
        with open('D:/new/photo_mir.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Кинозал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Брест, ул. Пушкинская, 7')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    elif message.text == 'Кинотеатр Восток' and selected_city == 'Гродно':
        with open('D:/new/photo_vostok.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Кинозал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гродно, пр-т Космонавтов, 41/1')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    elif message.text == 'К/т Красная звезда' and selected_city == 'Гродно':
        with open('D:/new/красная_звезда.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Кинозал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гродно, ул. Социалистическая, 4')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    elif message.text == 'Кинотеатр Октябрь' and selected_city == 'Гродно':
        with open('D:/new/октябрь_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Малый зал', 'VIP зал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гродно, ул. Поповича, 3')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'МЦ Гродно' and selected_city == 'Гродно':
        with open('D:/new/МЦ_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Кинозал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гродно, ул. Советская, 9')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    elif message.text == 'Кинотеатр Mooon' and selected_city == 'Гродно':
        with open('D:/new/moon.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1 Lounge', 'Зал 2 Premiere', 'Зал 3 Resto', 'Зал 4 VIP')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гродно, пр-т Янки Купалы, 87')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'Кинотеатр Мир' and selected_city == 'Гомель':
        with open('D:/new/kino_mir.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Видеозал', 'VIP зал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гомель, ул. Ильича, 51Б')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'К/т им. М.И.Калинина' and selected_city == 'Гомель':
        with open('D:/new/kino_kalinina.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Малый зал', 'МиниОН зал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гомель, ул. Коммунаров, 4')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'Кинотеатр Октябрь' and selected_city == 'Гомель':
        with open('D:/new/октябрь_гомель.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Кинозал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гомель, ул. Барыкина, 127')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    elif message.text == 'Кинотеатр Misteria' and selected_city == 'Гомель':
        with open('D:/new/мистерия.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Кинозал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Адрес: г.Гомель, ул. Юбилейная, 9')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    elif message.text == 'Драмтеатр' and selected_city == 'Брест':
        with open('D:/new/драм_театр_брест.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Малый зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Адрес: г.Брест, ул. Ленина, 21')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'Театр кукол' and selected_city == 'Брест':
        with open('D:/new/театр_кукол_брест.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Малый зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Адрес: г.Брест, ул. Ленина, 56')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'Драмтеатр' and selected_city == 'Гродно':
        with open('D:/new/драм_театр_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Малый зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Адрес: г.Гродно, ул. Мостовая, 35')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'Театр кукол' and selected_city == 'Гродно':
        with open('D:/new/театр_кукол_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зрительный зал', 'Камерный зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Адрес: г.Гродно, ул. Дзержинского, 1/1')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == 'Драмтеатр' and selected_city == 'Гомель':
        with open('D:/new/драм_театр_гомель.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Адрес: г.Гомель, пл. им. Ленина, 1')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    elif message.text == 'Театр кукол' and selected_city == 'Гомель':
        with open('D:/new/театр_кукол_гомель.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Адрес: г.Гомель, ул.Пушкина, 14')
        bot.send_message(message.chat.id, 'Выберите вариант👇', reply_markup=markup)
    if message.text == 'Драмтеатр':
        halls(message)


@bot.message_handler(func=lambda message: message.text in ['👈 Назад к выбору кинотеатра', '👈 Назад к выбору театра'])
def back_select_cinema(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    selected_city = dict_cities.get(message.chat.id)
    if message.text == '👈 Назад к выбору кинотеатра' and selected_city == 'Брест':
        markup.add('Кинотеатр Беларусь', 'Кинотеатр Мир')
        markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите кинотеатр', reply_markup=markup)
    elif message.text == '👈 Назад к выбору театра' and selected_city == 'Брест':
        markup.add('Драмтеатр', 'Театр кукол')
        markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите театр', reply_markup=markup)
    elif message.text == '👈 Назад к выбору кинотеатра' and selected_city == 'Гродно':
        markup.add('Кинотеатр Восток', 'К/т Красная звезда', 'Кинотеатр Октябрь', 'МЦ Гродно', 'Кинотеатр Mooon')
        markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите кинотеатр', reply_markup=markup)
    elif message.text == '👈 Назад к выбору театра' and selected_city == 'Гродно':
        markup.add('Драмтеатр', 'Театр кукол')
        markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите театр', reply_markup=markup)
    elif message.text == '👈 Назад к выбору кинотеатра' and selected_city == 'Гомель':
        markup.add('Кинотеатр Мир', 'К/т им. М.И.Калинина', 'Кинотеатр Октябрь', 'Кинотеатр Misteria')
        markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите кинотеатр', reply_markup=markup)
    elif message.text == '👈 Назад к выбору театра' and selected_city == 'Гомель':
        markup.add('Драмтеатр', 'Театр кукол')
        markup.add('👈 Назад к выбору кино и театр')
        bot.send_message(message.chat.id, 'Выберите театр', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Зал №1(Большой)', 'Зал №2(Малый)', 'Зал №3(VIP)',
                                                           'Кинозал', 'Большой зал', 'Малый зал', 'VIP зал',
                                                           'Зал 1 Lounge', 'Зал 2 Premiere', 'Зал 3 Resto',
                                                           'Зал 4 VIP', 'Видеозал', 'МиниОН зал',
                                                           'Зрительный зал', 'Камерный зал'])
def select_zal(message):
    zala = message.text
    dict_halls[message.chat.id] = zala
    selected_city = dict_cities.get(message.chat.id)
    kino_theater = dict_cinema.get(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Зал №1(Большой)' and selected_city == 'Брест':
        with open('E:/new/фото_большой_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Зал №2(Малый)' and selected_city == 'Брест':
        with open('D:/new/фото_малый_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Зал №3(VIP)' and selected_city == 'Брест':
        with open('D:/new/VIP_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Кинозал' and selected_city == 'Брест':
        with open('D:/new/фото_большой_зал_мир.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору кинотеатра')
    elif message.text == 'Кинозал' and selected_city == 'Гродно' and kino_theater == 'Кинотеатр Восток':
        with open('D:/new/зал_восток_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору кинотеатра')
    elif message.text == 'Кинозал' and selected_city == 'Гродно' and kino_theater == 'К/т Красная звезда':
        with open('D:/new/зал_красная_звезда.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору кинотеатра')
    elif message.text == 'Большой зал' and selected_city == 'Гродно' and kino_theater == 'Кинотеатр Октябрь':
        with open('D:/new/большой_зал_октябрь.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Малый зал' and selected_city == 'Гродно' and kino_theater == 'Кинотеатр Октябрь':
        with open('D:/new/октябрь_малый_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'VIP зал' and selected_city == 'Гродно':
        with open('D:/new/октябрь_VIP_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Кинозал' and selected_city == 'Гродно' and kino_theater == 'МЦ Гродно':
        with open('D:/new/МЦ_Гродно_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору кинотеатра')
    elif message.text == 'Зал 1 Lounge' and selected_city == 'Гродно':
        with open('D:/new/lounge_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Зал 2 Premiere' and selected_city == 'Гродно':
        with open('D:/new/premiere_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Зал 3 Resto' and selected_city == 'Гродно':
        with open('D:/new/resto_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Зал 4 VIP' and selected_city == 'Гродно':
        with open('D:/new/vip_зал_moon.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Большой зал' and selected_city == 'Гомель' and kino_theater == 'Кинотеатр Мир':
        with open('D:/new/большой_зал_мир.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Видеозал' and selected_city == 'Гомель':
        with open('D:/new/видео_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'VIP зал' and selected_city == 'Гомель':
        with open('D:/new/VIP_зал_мир.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Большой зал' and selected_city == 'Гомель' and kino_theater == 'К/т им. М.И.Калинина':
        with open('D:/new/большой_зал_калинина.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Малый зал' and selected_city == 'Гомель':
        with open('D:/new/малый_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'МиниОН зал' and selected_city == 'Гомель':
        with open('D:/new/миниОН_зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Кинозал' and selected_city == 'Гомель' and kino_theater == 'Кинотеатр Октябрь':
        with open('D:/new/октябрь_зал_гомель.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Цена', 'Купить билет')
        markup.add('👈 Назад к выбору кинотеатра')
    elif message.text == 'Кинозал' and selected_city == 'Гомель' and kino_theater == 'Кинотеатр Misteria':
        with open('D:/new/кинозал_мистерия.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору кинотеатра')
    elif message.text == 'Большой зал' and selected_city == 'Брест' and kino_theater == 'Драмтеатр':
        with open('D:/new/драм_театр_большая_сцена_брест.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Малый зал' and selected_city == 'Брест' and kino_theater == 'Драмтеатр':
        with open('D:/new/драм_театр_малая_сцена_брест.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Большой зал' and selected_city == 'Брест' and kino_theater == 'Театр кукол':
        with open('D:/new/театр_кукол_большая_брест.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Малый зал' and selected_city == 'Брест' and kino_theater == 'Театр кукол':
        with open('D:/new/театр_кукол_малая_брест.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Большой зал' and selected_city == 'Гродно' and kino_theater == 'Драмтеатр':
        with open('D:/new/драм_театр_большая_сцена_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Малый зал' and selected_city == 'Гродно' and kino_theater == 'Драмтеатр':
        with open('D:/new/драм_театр_малый_зал_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Зрительный зал' and selected_city == 'Гродно' and kino_theater == 'Театр кукол':
        with open('D:/new/зрительный_зал_театр_кукол_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Камерный зал' and selected_city == 'Гродно' and kino_theater == 'Театр кукол':
        with open('D:/new/камерный_зал_гродно.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору зала')
    elif message.text == 'Большой зал' and selected_city == 'Гомель' and kino_theater == 'Драмтеатр':
        with open('D:/new/драм_театр_большая_сцена_гомель.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору театра')
    elif message.text == 'Большой зал' and selected_city == 'Гомель' and kino_theater == 'Театр кукол':
        with open('D:/new/театр_кукол_зал_гомель.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('👈 Назад к выбору театра')
    bot.send_message(message.chat.id, 'Выберите кнопку👇', reply_markup=markup)
    if message.text in ['Большой зал', 'Малый зал', 'Камерный зал']:
        select_halls(message)


@bot.message_handler(func=lambda message: message.text == '👈 Назад к выбору зала')
def back_select_zal(message):
    selected_city = dict_cities.get(message.chat.id)
    kino_theater = dict_cinema.get(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == '👈 Назад к выбору зала' and selected_city == 'Брест' and kino_theater == 'Кинотеатр Беларусь':
        markup.add('Зал №1(Большой)', 'Зал №2(Малый)', 'Зал №3(VIP)')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Брест' and kino_theater == 'Драмтеатр':
        markup.add('Большой зал', 'Малый зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Брест' and kino_theater == 'Театр кукол':
        markup.add('Большой зал', 'Малый зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Гродно' and kino_theater == 'Кинотеатр Октябрь':
        markup.add('Большой зал', 'Малый зал', 'VIP зал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Гродно' and kino_theater == 'Кинотеатр Mooon':
        markup.add('Зал 1 Lounge', 'Зал 2 Premiere', 'Зал 3 Resto', 'Зал 4 VIP')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Гродно' and kino_theater == 'Драмтеатр':
        markup.add('Большой зал', 'Малый зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Гродно' and kino_theater == 'Театр кукол':
        markup.add('Зрительный зал', 'Камерный зал')
        markup.add('👈 Назад к выбору театра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Гомель' and kino_theater == 'Кинотеатр Мир':
        markup.add('Большой зал', 'Видеозал', 'VIP зал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif message.text == '👈 Назад к выбору зала' and selected_city == 'Гомель' and kino_theater == 'К/т им. М.И.Калинина':
        markup.add('Большой зал', 'Малый зал', 'МиниОН зал')
        markup.add('👈 Назад к выбору кинотеатра')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Афиша и Цена', 'Купить билет', 'Афиша и Купить билет', 'Афиша'])
def afisha_buy_ticket(message):
    selected_city = dict_cities.get(message.chat.id)
    zala = dict_halls.get(message.chat.id)
    kino_theater = dict_cinema.get(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Афиша и Цена':
        if selected_city == 'Брест' and zala == 'Зал №1(Большой)':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://kinobrest.by/pages/bol', reply_markup=markup)
        elif selected_city == 'Брест' and zala == 'Зал №2(Малый)':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://kinobrest.by/pages/mal', reply_markup=markup)
        elif selected_city == 'Брест' and zala == 'Зал №3(VIP)':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://kinobrest.by/pages/vip', reply_markup=markup)
        elif selected_city == 'Брест' and kino_theater == 'Кинотеатр Мир':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://kinobrest.by/pages/mir', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Кинотеатр Восток':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://grodno.in/cinema/east/afisha/', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'К/т Красная звезда':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://grodno.in/cinema/red-star/afisha/', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Кинотеатр Октябрь':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://grodno.in/cinema/october/afisha/', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'МЦ Гродно':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://grodno.in/club/mcgrodno/afisha/', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Кинотеатр Mooon':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://grodno.in/cinema/mooon/afisha/', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'Кинотеатр Мир':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://gomelkino.by/cinema/kinoteatr-mir/', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'К/т им. М.И.Калинина':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://gomelkino.by/cinema/kinoteatr-im-kalinina/', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'Кинотеатр Октябрь':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://gomelkino.by/cinema/k-t-oktyabr-3d-gomel/', reply_markup=markup)
    elif message.text == 'Купить билет':
        if selected_city == 'Брест' and zala == 'Зал №1(Большой)':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/place/id/109505/', reply_markup=markup)
        elif selected_city == 'Брест' and zala == 'Зал №2(Малый)':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/place/id/109505/', reply_markup=markup)
        elif selected_city == 'Брест' and zala == 'Зал №3(VIP)':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/place/id/109505/', reply_markup=markup)
        elif selected_city == 'Брест' and kino_theater == 'Кинотеатр Мир':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/place/id/109507/', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Кинотеатр Восток':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'http://kinoteatr.megamag.by/index.php?cPath=21141', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'К/т Красная звезда':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'http://kinoteatr.megamag.by/index.php?cPath=6397', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Кинотеатр Октябрь':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'http://kinoteatr.megamag.by/index.php?cPath=1&osCsid=4uojdohpl1jbd4b360i85iiqr1', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'МЦ Гродно':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'http://kinoteatr.megamag.by/index.php?cPath=1861425', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Кинотеатр Mooon':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/kino/grodno/', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'Кинотеатр Мир':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/kino/gomel/#?date_from=1686517200&date_to=0&options%5Bplace%5D=10082398', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'К/т им. М.И.Калинина':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/kino/gomel/#?date_from=1686517200&date_to=0&options%5Bplace%5D=109511', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'Кинотеатр Октябрь':
            markup.add('Афиша и Цена')
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/kino/gomel/#?date_from=1686517200&date_to=0&options%5Bplace%5D=109510', reply_markup=markup)
        elif selected_city == 'Брест' and kino_theater == 'Драмтеатр':
            markup.add('Афиша')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://www.kvitki.by/rus/razvlechenija/zali/brestskij-akademicheskij-teatr-dramy-5280/', reply_markup=markup)
    elif message.text == 'Афиша и Купить билет':
        if selected_city == 'Гомель' and kino_theater == 'Кинотеатр Misteria':
            markup.add('👈 Назад к выбору кинотеатра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://afisha.relax.by/kino/gomel/#?date_from=1686517200&date_to=0&options%5Bplace%5D=10744943', reply_markup=markup)
        elif selected_city == 'Брест' and kino_theater == 'Театр кукол':
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://puppet-brest.by/afisha/', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Драмтеатр':
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://drama-grodno.by/affiche/', reply_markup=markup)
        elif selected_city == 'Гродно' and kino_theater == 'Театр кукол':
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://grodnolyalka.by/events/list/', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'Драмтеатр':
            markup.add('👈 Назад к выбору театра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://gomeldrama.by/?page_id=15#afisha', reply_markup=markup)
        elif selected_city == 'Гомель' and kino_theater == 'Театр кукол':
            markup.add('👈 Назад к выбору театра')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'http://gomelpuppet.by/afisha.html', reply_markup=markup)
    elif message.text == 'Афиша':
        if selected_city == 'Брест' and kino_theater == 'Драмтеатр':
            markup.add('Купить билет')
            markup.add('👈 Назад к выбору зала')
            bot.send_message(message.chat.id, 'Нажмите на ссылку👇', reply_markup=markup)
            bot.send_message(message.chat.id, 'https://bresttheatre.info/repertuar.html', reply_markup=markup)
    if message.text in ['Купить билет', 'Афиша и Купить билет', 'Афиша']:
        buy_ticket(message)


######################### КОД ЭММЫ:


# создаем кнопки 'Кинотеатр', 'Театр', 'Вернуться к выбору города' во всех городах
@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text in ['Витебск', 'Могилев', 'Минск'])
def city_1(message):
    selected_city = message.text
    if selected_city == 'Витебск':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кинотеатры', 'Театры')
        markup.add('👈 Назад к выбору города')
        dict_cities[message.chat.id] = selected_city  # записывает в словарь названия городов
        bot.send_message(message.chat.id, 'Выберите, что интересует', reply_markup=markup)
    elif selected_city == 'Могилев':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кинотеатры', 'Театры')
        markup.add('👈 Назад к выбору города')
        dict_cities[message.chat.id] = selected_city
        bot.send_message(message.chat.id, 'Выберите, что интересует', reply_markup=markup)
    elif selected_city == 'Минск':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кинотеатры', 'Театры')
        markup.add('👈 Назад к выбору города')
        dict_cities[message.chat.id] = selected_city
        bot.send_message(message.chat.id, 'Выберите, что интересует', reply_markup=markup)


# функция для создания кнопок названий кинотеатров и театров для каждого города + кнопка "назад"
@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text in ['Кинотеатры', 'Театры'])
def cinema(message):
    selected_city = dict_cities.get(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Кинотеатры':
        if selected_city == 'Витебск':
            markup.add('Мир', 'Дом кино')
            markup.add('Назад')
        elif selected_city == 'Могилев':
            markup.add('Starlight', 'Космос', 'Родина', 'Чырвоная зорка')
            markup.add('Назад')
        elif selected_city == 'Минск':
            markup.add("Аврора", "Беларусь", "Берестье", "Дом кино")
            markup.add("Назад")
        bot.send_message(message.chat.id, 'Выберите кинотеатр', reply_markup=markup)
    elif message.text == 'Театры':
        if selected_city == 'Витебск':
            markup.add('Драмтеатр', 'Театр Лялька')
            markup.add('Назад')
        elif selected_city == 'Могилев':
            markup.add('Драмтеатр', 'Театр лялек')
            markup.add('Назад')
        elif selected_city == 'Минск':
            markup.add('Музыкальный', 'Большой', 'Театр лялек', 'Театр белорусской драматургии')
            markup.add('Назад')
        bot.send_message(message.chat.id, 'Выберите театр', reply_markup=markup)


# функция для кнопки "назад", возвращает в меню кнопок  выбора развлечений
# "Кинотеатр" и "театр" + "возврат к выбору города"
@bot.message_handler(func=lambda message: message.text == 'Назад')
def city_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    selected_city = dict_cities.get(message.chat.id)
    if selected_city == 'Витебск':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кинотеатры', 'Театры')
        markup.add('👈 Назад к выбору города')
    elif selected_city == 'Могилев':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кинотеатры', 'Театры')
        markup.add('👈 Назад к выбору города')
    elif selected_city == 'Минск':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кинотеатры', 'Театры')
        markup.add('👈 Назад к выбору города')
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


# функция для вывода фото и адреса выбранного кинотеатра, театра и возможность
# перехода к просмотру залов + "возврат"
@bot.message_handler(func=lambda message: message.text in ['Мир', 'Дом кино', 'Starlight', 'Космос',
                                                           'Родина', 'Чырвоная зорка', 'Аврора', 'Беларусь',
                                                           'Берестье', 'Драмтеатр', 'Театр Лялька', 'Театр лялек',
                                                           'Музыкальный', 'Большой', 'Театр белорусской драматургии'])
def halls(message):
    kino_theater = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dict_cinema[message.chat.id] = kino_theater  # записывает названия заведений в словарь
    selected_city = dict_cities.get(message.chat.id)
    if selected_city == 'Витебск' and message.text == 'Мир':
        bot.send_message(message.chat.id, 'Адрес: ул. Чехова, 3')
        with open('D:/ПИТОН/фото/mir.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Витебск' and message.text == 'Дом кино':
        bot.send_message(message.chat.id, 'Адрес: ул. Ленина, 40')
        with open('D:/ПИТОН/фото/дом кино.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Малый зал')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Starlight':
        bot.send_message(message.chat.id, 'Адрес: ул. Первомайская, 57(3 этаж)')
        with open('D:/ПИТОН/фото/starlight.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Кинозал 1 LUX', 'Кинозал 2 SWEET BOX', 'Кинозал 3 SMALL HALL',
                   'Кинозал 4 BIG HALL', 'Кинозал 5 ATMOS')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Космос':
        bot.send_message(message.chat.id, 'Адрес: пр-т Пушкинский, 10')
        with open('D:/ПИТОН/фото/космос.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Родина':
        bot.send_message(message.chat.id, 'Адрес: ул.Ленинская, 47')
        with open('D:/ПИТОН/фото/родина.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Чырвоная зорка':
        bot.send_message(message.chat.id, 'Адрес: ул. Первомайская, 14')
        with open('D:/ПИТОН/фото/чырвоная_зорка.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Аврора':
        bot.send_message(message.chat.id, 'Адрес: ул. Притыцкого, 23')
        with open('D:/ПИТОН/фото/аврора минск.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал красный', 'Зал лазурный', 'Зал комфорт')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Беларусь':
        bot.send_message(message.chat.id, 'Адрес: ул. Романовская Слобода, 28')
        with open('D:/ПИТОН/фото/минск беларусь.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1', 'Зал 2', 'Зал 3', 'Зал 4', 'Зал 5')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Берестье':
        bot.send_message(message.chat.id, 'Адрес: пр-т Газеты Правда, 25')
        with open('D:/ПИТОН/фото/минск берестье.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Дом кино':
        bot.send_message(message.chat.id, 'Адрес: ул. Толбухина, 18')
        with open('D:/ПИТОН/фото/минск дом кино.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал 1')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Витебск' and message.text == 'Драмтеатр':
        bot.send_message(message.chat.id, 'Адрес: ул. Замковая, 2')
        with open('D:/ПИТОН/фото/драмтеатр.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Камерный зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Витебск' and message.text == 'Театр Лялька':
        bot.send_message(message.chat.id, 'Адрес: ул. Пушкина, 2')
        with open('D:/ПИТОН/фото/Белорусский_театр_«Лялька».jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Драмтеатр':
        bot.send_message(message.chat.id, 'Адрес: ул. Первомайская, 7')
        with open('D:/ПИТОН/фото/могилев драмтеатр.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большая сцена', 'Малая сцена')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Театр лялек':
        bot.send_message(message.chat.id, 'Адрес: ул. Первомайская, 73')
        with open('D:/ПИТОН/фото/могилев театр лялек.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Музыкальный':
        bot.send_message(message.chat.id, 'Адрес:  ул. Мясникова, 44')
        with open('D:/ПИТОН/фото/минск музыкальный.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Большой':
        bot.send_message(message.chat.id, 'Адрес: пл. Парижской Коммуны, 1')
        with open('D:/ПИТОН/фото/минск большой.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Большой зал', 'Камерный зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Театр лялек':
        bot.send_message(message.chat.id, 'Адрес: ул. Энгельса, 20')
        with open('D:/ПИТОН/фото/минск татр лялек.png', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Театр белорусской драматургии':
        bot.send_message(message.chat.id, 'Адрес: пл. Парижской Коммуны, 1')
        with open('D:/ПИТОН/фото/минск драматургия.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите зал', reply_markup=markup)


# функция для кнопки "назад, возвращает в меню выбора кинотеатра, театра
@bot.message_handler(func=lambda message: message.text in ['Возврат к кинотеатрам', 'Возврат к театрам'])
def city_4(message):
    selected_city = dict_cities.get(message.chat.id)
    if selected_city == 'Витебск' and message.text == 'Возврат к кинотеатрам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Мир', 'Дом кино')
        markup.add('Назад')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Возврат к кинотеатрам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Starlight', 'Космос', 'Родина', 'Чырвоная зорка')
        markup.add('Назад')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Возврат к кинотеатрам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Аврора', 'Беларусь', 'Берестье', 'Дом кино')
        markup.add('Назад')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and message.text == 'Возврат к театрам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Драмтеатр', 'Театр Лялька')
        markup.add('Назад')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Возврат к театрам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Драмтеатр', 'Театр лялек')
        markup.add('Назад')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and message.text == 'Возврат к театрам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Музыкальный', 'Большой', 'Театр лялек', 'Театр белорусской драматургии')
        markup.add('Назад')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


# функция для просмотра фото залов + выбора для просмотра афиши, покупки билетов
@bot.message_handler(func=lambda message: message.text in ['Зал 1', 'Зал 2', 'Зал 3', 'Зал 4', 'Зал 5', 'Большой зал',
                                                           'Малый зал', 'Кинозал 1 LUX', 'Кинозал 2 SWEET BOX',
                                                           'Кинозал 3 SMALL HALL', 'Кинозал 4 BIG HALL',
                                                           'Кинозал 5 ATMOS', 'Зал лазурный', 'Зал комфорт',
                                                           'Зал красный', 'Камерный зал', 'Зал', 'Большая сцена',
                                                           'Малая сцена'])
def select_halls(message):
    selected_city = dict_cities.get(message.chat.id)
    kino_theater = dict_cinema.get(message.chat.id) # извлекает название заведения из словаря по ключу
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if selected_city == 'Витебск' and message.text == 'Зал 1':
        with open('D:/ПИТОН/фото/Mir_zal_2_1.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and message.text == 'Зал 2':
        with open('D:/ПИТОН/фото/Mir_zal_2_2.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Дом кино' and message.text == 'Большой зал':
        with open('D:/ПИТОН/фото/DK_zal_1_2.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and message.text == 'Малый зал':
        with open('D:/ПИТОН/фото/DK malzal.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Starlight' and message.text == 'Кинозал 1 LUX':
        with open('D:/ПИТОН/фото/Кинозал1 LUX.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Starlight' and message.text == 'Кинозал 2 SWEET BOX':
        with open('D:/ПИТОН/фото/sweet box.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Starlight' and message.text == 'Кинозал 3 SMALL HALL':
        with open('D:/ПИТОН/фото/small hall.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Starlight' and message.text == 'Кинозал 4 BIG HALL':
        with open('D:/ПИТОН/фото/big hall.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Starlight' and message.text == 'Кинозал 5 ATMOS':
        with open('D:/ПИТОН/фото/atmos.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Космос' and message.text == 'Зал 1':
        with open('D:/ПИТОН/фото/зал1 космос.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Космос' and message.text == 'Зал 2':
        with open('D:/ПИТОН/фото/зал2 космос.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Родина' and message.text == 'Зал 1':
        with open('D:/ПИТОН/фото/родина зал1.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Родина' and message.text == 'Зал 2':
        with open('D:/ПИТОН/фото/родина зал2.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Чырвоная зорка' and message.text == 'Зал 1':
        with open('D:/ПИТОН/фото/зал чырвоная зорка.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Аврора' and message.text == 'Зал красный':
        with open('D:/ПИТОН/фото/красный зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Аврора' and message.text == 'Зал лазурный':
        with open('D:/ПИТОН/фото/лазурный зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Аврора' and message.text == 'Зал комфорт':
        with open('D:/ПИТОН/фото/зал комфорт.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Беларусь' and message.text == 'Зал 1':
        with open('D:/ПИТОН/фото/зал1-беларусь.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Беларусь' and message.text == 'Зал 2':
        with open('D:/ПИТОН/фото/зал2 беларусь.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Беларусь' and message.text == 'Зал 3':
        with open('D:/ПИТОН/фото/зал3 беларусь.webp', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Беларусь' and message.text == 'Зал 4':
        with open('D:/ПИТОН/фото/зал4 беларусь.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Беларусь' and message.text == 'Зал 5':
        with open('D:/ПИТОН/фото/зал5 беларусь.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Берестье' and message.text == 'Зал 1':
        with open('D:/ПИТОН/фото/минск берестье зал 1.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Берестье' and message.text == 'Зал 2':
        with open('D:/ПИТОН/фото/минск берестье зал 2.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Дом кино' and message.text == 'Зал 1':
        with open('D:/ПИТОН/фото/минск дом кино зал1.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Драмтеатр' and message.text == 'Большой зал':
        with open('D:/ПИТОН/фото/vyalikaya_zala-3.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Драмтеатр' and message.text == 'Камерный зал':
        with open('D:/ПИТОН/фото/kamernaya_zala-6.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Театр Лялька' and message.text == 'Зал':
        with open('D:/ПИТОН/фото/зал лялька.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Драмтеатр' and message.text == 'Большая сцена':
        with open('D:/ПИТОН/фото/могилев драмтеатр большой зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Драмтеатр' and message.text == 'Малая сцена':
        with open('D:/ПИТОН/фото/могилев драмтеатр малая сцена.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Театр лялек' and message.text == 'Зал':
        with open('D:/ПИТОН/фото/могилев лялька зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Музыкальный' and message.text == 'Зал':
        with open('D:/ПИТОН/фото/минск музыкальный зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша', 'Купить билет')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Большой' and message.text == 'Большой зал':
        with open('D:/ПИТОН/фото/минск большой зал1.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Большой' and message.text == 'Камерный зал':
        with open('D:/ПИТОН/фото/минск большой камерный.webp', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Назад к выбору зала')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Театр лялек' and message.text == 'Зал':
        with open('D:/ПИТОН/фото/минск театр лялек зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Театр белорусской драматургии' and message.text == 'Зал':
        with open('D:/ПИТОН/фото/минск драматургия зал.jpg', 'rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f)
        markup.add('Афиша и Купить билет')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


# функция для кнопки "назад к залам", возвращает к выбору зала
# и возможность возврата к выбору кинотеатра, театра
@bot.message_handler(func=lambda message: message.text == 'Назад к выбору зала')
def city_5(message):
    selected_city = dict_cities.get(message.chat.id)
    kino_theater = dict_cinema.get(message.chat.id)
    if selected_city == 'Витебск' and kino_theater == 'Мир' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Дом кино' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Большой зал', 'Малый зал')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Starlight' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кинозал 1 LUX', 'Кинозал 2 SWEET BOX',
                   'Кинозал 3 SMALL HALL', 'Кинозал 4 BIG HALL', 'Кинозал 5 ATMOS')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Космос' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Родина' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Чырвоная зорка' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал 1')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Аврора' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал красный', 'Зал лазурный', 'Зал комфорт')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Беларусь' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал 1', 'Зал 2', 'Зал 3', 'Зал 4', 'Зал 5')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Берестье' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал 1', 'Зал 2')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Дом кино' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал 1')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Драмтеатр' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Большой зал', 'Камерный зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Театр Лялька' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Драмтеатр' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Большая сцена', 'Малая сцена')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Театр лялек' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Музыкальный' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Большой' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Большой зал', 'Камерный зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Театр лялек' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Театр белорусской драматургии' and message.text == 'Назад к выбору зала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Зал')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


# функция для просмотра афиши и покупки билетов кинотеатров, театров
@bot.message_handler(func=lambda message: message.text in ['Афиша', 'Купить билет', 'Афиша и Купить билет'])
def buy_ticket(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    selected_city = dict_cities.get(message.chat.id)
    kino_theater = dict_cinema.get(message.chat.id)
    if selected_city == 'Витебск' and message.text == 'Афиша':
        markup.add('Купить билет')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'http://kino.vitebsk.by', reply_markup=markup)
    elif selected_city == 'Витебск' and message.text == 'Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://24afisha.by/ru/vitebsk/events/kino?view=today', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Афиша':
        markup.add('Купить билет')
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://starcinema.by', reply_markup=markup)
    elif selected_city == 'Могилев' and message.text == 'Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://starcinema.by/afisha', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Космос' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'http://mogilevkino.by/objects/2', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Родина' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'http://mogilevkino.by/objects/3', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Чырвоная зорка' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'http://mogilevkino.by/objects/4', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Аврора' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://kinominska.by/objects/26', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Беларусь' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://kinominska.by/objects/27', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Берестье' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://kinominska.by/objects/16', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Дом кино' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к кинотеатрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://kinominska.by/objects/15', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Драмтеатр' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://kolastheatre.by/ru/afisha', reply_markup=markup)
    elif selected_city == 'Витебск' and kino_theater == 'Театр Лялька' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://lialka.by/kvitki/', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Драмтеатр' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'http://kinoteatr.megamag.by/index.php?cPath=198213', reply_markup=markup)
    elif selected_city == 'Могилев' and kino_theater == 'Театр лялек' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'http://www.teatrkukol.by/афиша/', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Музыкальный' and message.text == 'Афиша':
        markup.add('Купить билет')
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://musicaltheatre.by/afisha', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Музыкальный' and message.text == 'Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://tce.by/?base=NzY1ODNDOEEtQjBGNS00OUZCLTg5NjYtQkZEQ0IwRDdBODI2', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Большой' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://bolshoibelarus.by/rus/afisha-ru/-.html', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Театр лялек' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://puppet-minsk.com/afisha', reply_markup=markup)
    elif selected_city == 'Минск' and kino_theater == 'Театр белорусской драматургии' and message.text == 'Афиша и Купить билет':
        markup.add('Возврат к театрам')
        bot.send_message(message.chat.id, 'Нажмите на ссылку', reply_markup=markup)
        bot.send_message(message.chat.id, 'https://rtbd.by/afisha/', reply_markup=markup)

# Запускаем бот
bot.polling(none_stop=True)
