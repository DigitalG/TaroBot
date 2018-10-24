import telebot
from telebot import types
import parse

bot = telebot.TeleBot("")

titles = ['Общее значение', 'Личностное состояние', 'На более глубоком уровне', 'Проффесиональная ситуация',
          'Финансовое положение', 'Личные отношения', 'Состояние здоровья', 'Перевернутая карта',
          'Проявления в сочетаниях', ' Архетипические соответствия', 'Копилка наблюдений']


def parse_pg():
    f = open('result.txt', 'r')
    info = f.read().split('---')
    for i in range(len(info)):
        info[i] = info[i].replace('\n\n', '\n').replace('\n\n', '\n')
    return info


def check_card(str):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
               '19', '20', '21']
    name = {'жезлов': 'staff',
            'мечей': 'sword',
            'чаш': 'cup',
            'пентаклей': 'coin'}

    if str in numbers:
        dic = {}
        f = open('cards.txt', 'r')
        a = f.readline().split(' ')
        b = f.readline().split(' ')
        for i in range(len(a)):
            dic[a[i]] = b[i]
        return dic[str]
    else:
        dic = {}
        tmp = str.lower().split(' ')
        file = name[tmp[1]] + '.txt'
        f = open(file, 'r')
        a = f.readline().split(' ')
        b = f.readline().split(' ')
        for i in range(len(a)):
            dic[a[i]] = b[i]
        return dic[tmp[0]]


def check_str(str):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
               '19', '20', '21']
    if str in numbers:
        return True
    else:
        tmp = str.lower().split(' ')
        if tmp[0] in numbers or tmp[0] in ['туз', 'паж', 'рыцарь', 'дама', 'король']:
            if tmp[1] in ['чаш', 'мечей', 'жезлов', 'пентаклей']:
                return True
        else:
            return False


chosen_card = '0'


@bot.message_handler(func=lambda m: m.text in titles)
def choose_handler(message):
    print(message.text)
    choose = message.text
    i = titles.index(choose)
    if len(parse_pg()[i+1]) >2000:
        k = len(parse_pg()[i+1])//2000 + 1
        print(k)
        tmp = []
        for i in range(k):
            tmp.append(parse_pg()[i+1][i:i+2000])
        for msg in tmp:
            bot.send_message(message.chat.id, '--' + msg)
            #print(msg)
    else:
        bot.send_message(message.chat.id,'--' +  parse_pg()[i+1])
    bot.send_message(message.chat.id, '--' + parse_pg()[i + 1])


@bot.message_handler(func=lambda m: check_str(m.text))
def main_handler(message):
    print(message.text)
    chosen_card = check_card(message.text)
    parse.parse(chosen_card)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    for t in titles:
        itembtn = types.KeyboardButton(t)
        markup.add(itembtn)
    bot.send_message(message.chat.id, "Выбери значение:", reply_markup=markup)


bot.polling()
