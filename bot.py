#!/usr/bin/python3

# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import config
import calc

#TODO:implements connect logging and out debug strings
#import logging

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

def answer_key():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    markup.row('Ввести точное значение')
    markup.row('Расчитать')
    return markup

def select_result(message):
    result = calc.Calculator(DATA)
    result.set_error_device(DATA['error_device'])
    x = result.get_small_result()[0]
    delt_x = result.get_small_result()[1]
    eps = result.get_small_result()[2]
    if message.text == 'Коротко':
        out_string = '\U000025B6 Результат:\n\U000025FB x = {0} +/- {1}\n'.format(x,delt_x)
        out_string += '\U000025B6 Относительная погрешность:\n\U000025FB{}\n'.format(eps)
        msg = bot.send_message(message.chat.id,out_string)
    else:
        out_string = '\U000025B6 Среднее арфиметическое:\n\U000025FB{}\n'.format(round(result.details()['average_summ'],5))
        i = 1
        out_string += '\U00002B07 Случайная погрешность для каждого\n'
        for elem in result.details()['rand_error']:
            out_string += '\t\U000025B6 Измерение №{0}:\n\t\U000025FB {1}\n'.format(i,round(elem,5))
            i +=1
        out_string += '\U00002B07 Квадраты погрешностей\n'
        i = 1
        for qtr in result.details()['qtrs']:
            out_string += '\t\U000025B6 Погрешность №{0}:\n\t\U000025FB {1}\n'.format(i,round(qtr,12))
            i +=1
        out_string += '\U000025B6 Средняя квадратичная погрешность:\n\U000025FB {}\n'.format(round(result.details()['average_qtr'],5))
        out_string += '\U000025B6 Средняя квадратичная всего результата:\n\U000025FB {}\n'.format(round(result.details()['all_average'],5))
        out_string += '\U000025B6 Случайная погрешность:\n\U000025FB {}\n'.format(round(result.details()['random_error'],5))
        out_string += '\U000025B6 Погрешность округления:\n\U000025FB {}\n'.format(result.error_device)
        out_string += '\U000025B6 Полная абсолютная погрешность измерений:\n\U000025FB {}\n'.format(round(result.details()['full_error'],5))
        out_string += '\U000025B6 Относительная погрешность результата:\n\U000025FB {}\n'.format(round(result.details()['eps_error'],5))
        out_string += '\U000025B6 Конечный результат:\n'
        out_string += '\U000025FB x = {0} +/- {1}\n'.format(x,delt_x)
        out_string += '\U000025B6 eps:{}'.format(eps)
        msg = bot.send_message(message.chat.id,out_string)

def input_error_round(message):
    DATA['error_round'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'Готово!\U0001F60A В какой форме вам нужен результат?', reply_markup = result_key())
    bot.register_next_step_handler(msg,select_result)

def helper_h(message):
    DATA['error_device']['h'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'И последнее - ошибка округления.')
    bot.register_next_step_handler(msg,input_error_round)

def helper_p(message):
    DATA['error_device'] = {}
    DATA['error_device']['p'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'Цена деления прибора:')
    bot.register_next_step_handler(msg,helper_h)

def helper_err(message):
    DATA['error_device'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'И последнее - ошибка округления.')
    bot.register_next_step_handler(msg,input_error_round)

def input_error_device(message):
    if message.text == 'Расчитать':
        msg = bot.send_message(message.chat.id, 'Интервал вероятности:')
        bot.register_next_step_handler(msg,helper_p)
    else:
        bot.register_next_step_handler(message,helper_err)

def coeff(message):
    if message.text != '/help_st':
        DATA['st'] = float(message.text)
        msg = bot.send_message(message.chat.id, 'Осталось чуть-чуть. Введите ошибку прибора\U0001F609',reply_markup=answer_key())
        bot.register_next_step_handler(msg,input_error_device)
    else:
        #TODO: implements help for coeff st
        bot.register_next_step_handler(message,help_st)

def check_value(message):
    if DATA['iter'] <= DATA['count']-1:
        DATA['array'].append(float(message.text))
        DATA['iter'] += 1
        msg = bot.send_message(message.chat.id,'\U00002611 Значение №'+str(DATA['iter'])+':')
        bot.register_next_step_handler(msg,check_value)
    else:
        DATA['array'].append(float(message.text))
        msg = bot.send_message(message.chat.id, '\U0001F60C Введите коэффицент Стьюдента:\n\U00002753 Не можете вспомнить?\n /help_st - уточните.')
        bot.register_next_step_handler(msg,coeff)

def count_step(message):
    may_count = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
    chat_id = message.chat.id
    if message.text in may_count:
        DATA['count'] = int(message.text)
        msg = bot.send_message(message.chat.id, '\U0001F609 Отлично! Теперь необходимы выши значения. Начнем с {} значения'.format(DATA['iter']))
        bot.register_next_step_handler(msg,check_value)
    else:
        msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..', reply_markup = get_keyboard())
        bot.register_next_step_handler(msg, count_step(msg,DATA['count']))

#TODO: implements simple start with all commands
#TODO: implements full help for work with bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    out = config.get_start()
    msg = bot.send_message(message.chat.id, out)

@bot.message_handler(commands=['help'])
def help_message(message):
    out = config.get_help()
    msg = bot.send_message(message.chat.id, out)

@bot.message_handler(commands=['/help_st'])
def help_st(message):
    msg = bot.send_message(message.chat.id, 'Я в хелпере стьюдента!')

@bot.message_handler(commands=['calc'])
def calc_operations(message):
    DATA['array'] = []
    DATA['iter'] = 1
    #TODO: implement check input string
    msg = bot.send_message(message.chat.id, "Мне нужно знать ваше количество измерений\U0001F60C", reply_markup=get_keyboard())
    bot.register_next_step_handler(msg, count_step)

if __name__ == '__main__':
    bot.polling()
