import time
from os import getenv
import telebot
from telebot import types
import wget
import xlrd
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

token = getenv('TOKEN')
bot = telebot.TeleBot(token)

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('sport_bot/sport-bot-439010-d1a421f189c0.json', scopes=scopes)
client = gspread.authorize(credentials)



class Score:
    def __init__(self, options=None
                 ):
        if options is None:
            options = {
                '1. Жим гири': ['Нет рекордсмена', 0],
                '2. Махи гири': ['Нет рекордсмена', 0],
                '3. Приседания с гирей': ['Нет рекордсмена', 0],
                '4. Отжимания': ['Нет рекордсмена', 0],
                '5. Пресс': ['Нет рекордсмена', 0],
                '6. Прыжки на скакалке': ['Нет рекордсмена', 0],
                '7. Рывок гири': ['Нет рекордсмена', 0],
                '8. Прыгающий Джек': ['Нет рекордсмена', 0],
                '9. Приседания': ['Нет рекордсмена', 0]
            }
        self.options = options

class User:
    def __init__(self, user_id=None, location=None):
        self.location = location
        self.user_id = user_id



@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/Настройки")
    btn2 = types.KeyboardButton("/Отчет")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     f'Здравствуй, {message.from_user.first_name}, доступные команды:\n'
                     f'/Настройки - позволяет изменить локацию\n'
                     f'/Отчет - Позволяет загрузить таблицу и получить отчет',
                     reply_markup=markup)


@bot.message_handler(commands=['Настройки'])
def settings(message):
    markup = types.InlineKeyboardMarkup()
    locations = [
        '1.г.Зеленоград, ЗелАО, Бульварная зона16-мкрн. (у корп. 1606)',
        '2. г.Москва, СЗАО, ул. Митинская, вл. 31',
        '3. г.Москва, СЗАО, пересечение ул. Соколово-Мещерская и ул. Юровская',
        '4. г.Москва, САО, Коптевский бульвар, вл. 18 (парк «Бригантина»)',
        '5. г.Москва, ВАО, сквер у Гольяновского пруда',
        '6. г.Москва, ВАО, ул. Городецкая, вл. 1',
        '7. г.Москва, ВАО, ул.Святоозерская, вл. 1',
        '8. г.Москва, ВАО, ул. Вешняковская, вл. 16',
        '9. г.Москва, СВАО, Пересечение ул. Молодцова и ул. Сухонская (Бабушкинский парк)',
        '10. г.Москва, СВАО, Сквер по ул. Хачатуряна (ул. Хачатуряна, вл.13)',
        '11. г.Москва, ЮВАО, площадь Славы (Волгоградский пр-т, вл.119)',
        '12. г.Москва, ЮВАО, сквер у ст. метро "Некрасовка"',
        '13. г.Москва, ЮВАО, ул. Перерва, вл. 52',
        '14. г.Москва, ЮАО, ст.м. "Алма-Атинская" (ул. Ключевая, вл. 22, к.1)',
        '15. г.Москва, ЮАО, Ореховый б-р, вл. 24, стр.1',
        '16. г.Москва, ЮЗАО, бульвар Дмитрия Донского, вл. 11',
        '17. г.Москва, ЮЗАО, ул. Профсоюзная, вл. 41',
        '18. г.Москва, ЮЗАО, ул. Адмирала Руднева, вл. 8',
        '19. г.Москва, ЮЗАО, ул. Теплый стан, вл. 1Б',
        '20. г.Москва, ЗАО, ул. Матвеевская, вл. 2',
        '21. г.Москва, СВАО, Проезд Серебрякова, д. 14, стр.23 (напротив)',
        '22. г.Москва, ЗАО, Мичуринский проспект, Олимпийская деревня, вл. 4',
        '23. г.Москва, СЗАО, ул.Авиационная, вл.24',
        '24. г.Москва, СВАО, ул.Грекова, вл.ЗЖ',
        '25. г.Москва, ЮВАО, Люблино, ул Краснодарская вл 66'
    ]
    for i in locations:
        btn = types.InlineKeyboardButton(text=str(i), callback_data=str(str(i).split()[0][:-1]))
        markup.add(btn)
    bot.send_message(message.chat.id, 'Выберите нужную вам локацию:', reply_markup=markup)


@bot.callback_query_handler()
def callback_worker(call):
    locations = [
        '1.г.Зеленоград, ЗелАО, Бульварная зона16-мкрн. (у корп. 1606)',
        '2. г.Москва, СЗАО, ул. Митинская, вл. 31',
        '3. г.Москва, СЗАО, пересечение ул. Соколово-Мещерская и ул. Юровская',
        '4. г.Москва, САО, Коптевский бульвар, вл. 18 (парк «Бригантина»)',
        '5. г.Москва, ВАО, сквер у Гольяновского пруда',
        '6. г.Москва, ВАО, ул. Городецкая, вл. 1',
        '7. г.Москва, ВАО, ул.Святоозерская, вл. 1',
        '8. г.Москва, ВАО, ул. Вешняковская, вл. 16',
        '9. г.Москва, СВАО, Пересечение ул. Молодцова и ул. Сухонская (Бабушкинский парк)',
        '10. г.Москва, СВАО, Сквер по ул. Хачатуряна (ул. Хачатуряна, вл.13)',
        '11. г.Москва, ЮВАО, площадь Славы (Волгоградский пр-т, вл.119)',
        '12. г.Москва, ЮВАО, сквер у ст. метро "Некрасовка"',
        '13. г.Москва, ЮВАО, ул. Перерва, вл. 52',
        '14. г.Москва, ЮАО, ст.м. "Алма-Атинская" (ул. Ключевая, вл. 22, к.1)',
        '15. г.Москва, ЮАО, Ореховый б-р, вл. 24, стр.1',
        '16. г.Москва, ЮЗАО, бульвар Дмитрия Донского, вл. 11',
        '17. г.Москва, ЮЗАО, ул. Профсоюзная, вл. 41',
        '18. г.Москва, ЮЗАО, ул. Адмирала Руднева, вл. 8',
        '19. г.Москва, ЮЗАО, ул. Теплый стан, вл. 1Б',
        '20. г.Москва, ЗАО, ул. Матвеевская, вл. 2',
        '21. г.Москва, СВАО, Проезд Серебрякова, д. 14, стр.23 (напротив)',
        '22. г.Москва, ЗАО, Мичуринский проспект, Олимпийская деревня, вл. 4',
        '23. г.Москва, СЗАО, ул.Авиационная, вл.24',
        '24. г.Москва, СВАО, ул.Грекова, вл.ЗЖ',
        '25. г.Москва, ЮВАО, Люблино, ул Краснодарская вл 66'
    ]
    for i in locations:
        if call.data == str(str(i).split()[0][:-1]):
            location = locations[int(call.data)-1]
            for i in DATA:
                if int(call.message.chat.id) == int(i.user_id):
                    i.location = location
            else:
                DATA.append(User(user_id=call.message.chat.id, location=location))
            bot.send_message(call.message.chat.id, f'локация изменена на {location}')
            break



def chose_location(message, locations):
    if message.text in locations:
        location = message.text
        bot.send_message(message.chat.id, f'локация изменена на {location}')
    else:
        bot.send_message(message.chat.id, 'Локация указана не верно повторите попытку')
        bot.register_next_step_handler(message, locations)


@bot.message_handler(commands=['Отчет'])
def report(message):
    bot.send_message(message.chat.id, 'Отправьте ссылку на гугл таблицу:')
    bot.register_next_step_handler(message, processing_report)


def processing_report(message):
    for i in DATA:
        if int(message.chat.id) == int(i.user_id):
            location = i.location
            print(location)
            break
    else:
        bot.send_message(message.chat.id, 'Локация не выбрана. Перенос на выбор локации...')
        settings(message)
        return False


    sheet = client.open_by_url(str(message.text))
    worksheet = sheet.get_worksheet(0)
    data = worksheet.get_all_values()

    # Создаем DataFrame с заголовками из первой строки таблицы
    df = pd.DataFrame(data[1:], columns=data[0])

    score_ch_male = Score()
    score_ch_female = Score()
    score_ma_male = Score()
    score_ma_female = Score()
    sex = ''
    age = ''
    k = 0

    # Обходим строки DataFrame, используя .iloc
    for i, row in df.iterrows():
        k += 1
        try:
            # Проверяем пол, используя .iloc
            if row.iloc[1] == 'жен':
                sex = 'female'
            elif row.iloc[1] == 'муж':
                sex = 'male'

            # Проверяем возраст, используя .iloc
            try:
                vozr=int(row.iloc[3])
                if vozr <= 17:
                    age = 'ch'
                elif vozr > 17:
                    age = 'ma'
            except:
                age=''

            # Логика проверки и обновления значений
            if age == 'ch':
                if sex == 'female':
                    if score_ch_female.options[row.iloc[6]][1] < int(row.iloc[7]):
                        score_ch_female.options[row.iloc[6]] = [row.iloc[2], int(row.iloc[7])]
                elif sex == 'male':
                    if score_ch_male.options[row.iloc[6]][1] < int(row.iloc[7]):
                        score_ch_male.options[row.iloc[6]] = [row.iloc[2], int(row.iloc[7])]
            elif age == 'ma':
                if sex == 'female':
                    if score_ma_female.options[row.iloc[6]][1] < int(row.iloc[7]):
                        score_ma_female.options[row.iloc[6]] = [row.iloc[2], int(row.iloc[7])]
                elif sex == 'male':
                    if score_ma_male.options[row.iloc[6]][1] < int(row.iloc[7]):
                        score_ma_male.options[row.iloc[6]] = [row.iloc[2], int(row.iloc[7])]
        except Exception as e:
            print(f"Error on row {k}: {e}")
              # Пропускаем строку в случае ошибки



    # Генерация контента для отправки в Telegram
    content = (f'🛑 РЕКОРД ДНЯ🔝\n\n'
               f'📍Локация: {location}\n\n'
               f'Рекорд дня от {sheet.title}\n\n')
    content += 'Категория: Дети\n\n'

    names = list(score_ch_male.options)
    for i in range(min(9, len(names))):
        content += (f'Дисциплина {names[i]}:\n'
                    f'М. - {score_ch_male.options[names[i]][0]} - {score_ch_male.options[names[i]][1]}\n')
        content += (f'Ж. - {score_ch_female.options[names[i]][0]} - {score_ch_female.options[names[i]][1]}\n\n')

    content += 'Категория: Взрослые\n\n'
    for i in range(min(9, len(names))):
        content += (f'Дисциплина {names[i]}:\n'
                    f'М. - {score_ma_male.options[names[i]][0]} - {score_ma_male.options[names[i]][1]}\n')
        content += (f'Ж. - {score_ma_female.options[names[i]][0]} - {score_ma_female.options[names[i]][1]}\n\n')


    bot.send_message(message.chat.id, content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    DATA=[]
    while True:
        try:
            bot.polling(none_stop=True)
            time.sleep(5)
        except Exception as e:
            print(e)
