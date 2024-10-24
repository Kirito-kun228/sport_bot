from os import getenv
import telebot
from telebot import types
import wget
import xlrd

token = getenv('TOKEN')
bot = telebot.TeleBot(token)


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
            bot.send_message(call.message.chat.id, f'локация изменена на {location}')



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
    #url = message.text
    #wget.download(url)
    book = xlrd.open_workbook('7.10.xls')
    sheet = book.sheet_by_index(0)
    lst = list(sheet.get_rows())
    score_ch_male = Score()
    score_ch_female = Score()
    score_ma_male = Score()
    score_ma_female = Score()
    sex = ''
    age = ''
    print(lst)
    k=0
    for row in lst:
        k+=1
        print(k)
        try:
            if row[1].value == 'жен':
                sex = 'female'
            elif row[1].value=='муж':
                sex = 'male'
            if row[3].value <= 17:
                age = 'ch'
            elif row[3].value > 17:
                age = 'ma'
            if age == 'ch':
                if sex == 'female':
                    if score_ch_female.options[row[6].value][1] < row[7].value:
                        score_ch_female.options[row[6].value] = [row[2].value, row[7].value]
                elif sex == 'male':
                    if score_ch_male.options[row[6].value][1] < row[7].value:
                        score_ch_male.options[row[6].value] = [row[2].value, row[7].value]
            elif age == 'ma':
                if sex == 'female':
                    if score_ma_female.options[row[6].value][1] < row[7].value:
                        score_ma_female.options[row[6].value] = [row[2].value, row[7].value]
                elif sex == 'male':
                    if score_ma_male.options[row[6].value][1] < row[7].value:
                        score_ma_male.options[row[6].value] = [row[2].value, row[7].value]
        except:
            ...
        print('test')

    print(1)
    content=(f'🛑 РЕКОРД ДНЯ🔝\n\n'
             f'📍Локация:\n\n'
             f'Рекорд дня от\n\n')
    content+='Категория: Дети\n\n'
    names=list(score_ch_male.options)

    for i in range(9):
        content+=(f'Дисциплина {names[i]}:\n'
                    f'М. - {score_ch_male.options[names[i]][0]} - {score_ch_male.options[names[i]][1]}\n')
        content += (f'Ж. - {score_ch_female.options[names[i]][0]} - {score_ch_female.options[names[i]][1]}\n\n')
    content+=f'Категория: Взрослые:\n\n'
    for i in range(9):
        content+=(f'Дисциплина {names[i]}:\n'
                    f'М. - {score_ma_male.options[names[i]][0]} - {score_ma_male.options[names[i]][1]}\n')
        content += (f'Ж. - {score_ma_female.options[names[i]][0]} - {score_ma_female.options[names[i]][1]}\n\n')


    bot.send_message(message.chat.id, content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
