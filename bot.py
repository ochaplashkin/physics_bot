#!/usr/bin/python3

import telebot
from telebot import types
import time
import config
import calc

TOKEN = config.get_token()

bot = telebot.TeleBot(TOKEN)

DATA = {}

def get_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    markup.row('1', '2','3','4')
    markup.row('5', '6', '7','8')
    markup.row('9', '10', '11','12')
    markup.row('13','14','15','16')
    return markup

def result_key():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    markup.row('Коротко')
    markup.row('Подробно')
    return markup

def select_result(message):
    print('Select_result',message.text)
    if message.text == 'Коротко':
        #TODO:implements out short result
        print('Выбран короткий результат')
    else:
        #TODO:implement out detail result
        print('Выбран подробный результат')

def input_error_round(message):
    DATA['error_round'] = float(message.text)
    print('Input_error',message.text)
    msg = bot.send_message(message.chat.id, 'А я уже всё посчитал :) Какой вам нужен результат?', reply_markup = result_key())
    bot.register_next_step_handler(msg,select_result)

def input_error_device(message):
    DATA['error_device'] = float(message.text)
    print('Input_error:',message.text)
    msg = bot.send_message(message.chat.id, 'И последнее: ошибка округления.')
    bot.register_next_step_handler(msg,input_error_round)

def coeff(message):
    print('Coeff:',message.text)
    DATA['st'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'Осталось чуть-чуть. Напишите ошибку прибора:')
    bot.register_next_step_handler(msg,input_error_device)

def check_value(message):
    print('Check:',message.text)
    if DATA['iter'] <= DATA['count']-1:
        DATA['array'].append(float(message.text))
        DATA['test'] += 1
        msg = bot.send_message(message.chat.id, 'Введите '+str(DATA['test'])+' значение')
        bot.register_next_step_handler(msg,check_value)
    else:
        msg = bot.send_message(message.chat.id, 'Я всё записал! Теперь скажите мне коэффицент Стьюдента:')
        bot.register_next_step_handler(msg,coeff)

def count_step(message):
    print('Count: ',message.text)
    may_count = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
    chat_id = message.chat.id
    if message.text in may_count:
        DATA['count'] = int(message.text)
        msg = bot.send_message(message.chat.id, 'Отлично! Теперь необходимы значения. Начнем c {} значения'.format(DATA['iter']))
        bot.register_next_step_handler(msg,check_value)
    else:
        msg = bot.send_message(message.chat.id, 'Нет, нет. Я жду от Вас число:', reply_markup = get_keyboard())
        bot.register_next_step_handler(msg, count_step(msg,DATA['count']))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    out = config.get_start()
    msg = bot.send_message(message.chat.id, out)

@bot.message_handler(commands=['help'])
def help_message(message):
    out = config.get_help()
    msg = bot.send_message(message.chat.id, out)


@bot.message_handler(commands=['calc'])
def calc_operations(message):
    DATA['array'] = []
    DATA['iter'] = 1
    #TODO: implement input/output results from calc.py
    msg = bot.send_message(message.chat.id, "Для начала, мне нужно знать ваше количество измерений:", reply_markup=get_keyboard())
    bot.register_next_step_handler(msg, count_step)

if __name__ == '__main__':
    bot.polling()
