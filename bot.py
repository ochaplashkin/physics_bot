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

def select_result(message):
    result = calc.Calculator(DATA)
    x = result.get_small_result()[0]
    delt_x = result.get_small_result()[1]
    eps = result.get_small_result()[2]
    if message.text == 'Коротко':
        out_string = 'Результат:\n x = {0} +/- {1}\n'.format(x,delt_x)
        out_string += 'Относительная погрешность:\n{}\n'.format(eps)
        msg = bot.send_message(message.chat.id,out_string)
    else:
        out_string = 'Среднее арфиметическое:\n{}\n'.format(round(result.details()['average_summ'],5))
        i = 1
        out_string += 'Случайная погрешность для каждого:\n'
        for elem in result.details()['rand_error']:
            out_string += 'Случайная погрешность для {0}:\n{1}\n'.format(i,round(elem,5))
            i +=1
        out_string += 'Квадраты погрешностей:\n'
        i = 1
        for qtr in result.details()['qtrs']:
            out_string += 'Для {0}:\n{1}\n'.format(i,round(qtr,12))
            i +=1
        out_string += 'Средняя квадратичная погрешность:\n{}\n'.format(round(result.details()['average_qtr'],5))
        out_string += 'Средняя квадратичная всего результата:\n{}\n'.format(round(result.details()['all_average'],5))
        out_string += 'Случайная погрешность:\n{}\n'.format(round(result.details()['random_error'],5))
        #TODO: Implement selection entering error device as p*(h/2)
        out_string += 'Погрешность округления:\n{}\n'.format(round(result.error_device,5))
        out_string += 'Полная абсолютная погрешность измерений:\n{}\n'.format(round(result.details()['full_error'],5))
        out_string += 'Относительная погрешность результата:\n{}\n'.format(round(result.details()['eps_error'],5))
        out_string += 'Конечный результат:\n'
        out_string += ' x = {0} +/- {1}\n'.format(x,delt_x)
        out_string += 'eps:{}'.format(eps)
        msg = bot.send_message(message.chat.id,out_string)

def input_error_round(message):
    DATA['error_round'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'Готово!\U0001F60A В какой форме вам нужен результат?', reply_markup = result_key())
    bot.register_next_step_handler(msg,select_result)

def input_error_device(message):
    DATA['error_device'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'И последнее - ошибка округления.')
    bot.register_next_step_handler(msg,input_error_round)

def coeff(message):
    DATA['st'] = float(message.text)
    msg = bot.send_message(message.chat.id, 'Осталось чуть-чуть. Введите ошибку прибора\U0001F609')
    bot.register_next_step_handler(msg,input_error_device)

def check_value(message):
    if DATA['iter'] <= DATA['count']-1:
        DATA['array'].append(float(message.text))
        DATA['iter'] += 1
        msg = bot.send_message(message.chat.id,'\U000027A1 '+str(DATA['iter'])+' значение')
        bot.register_next_step_handler(msg,check_value)
    else:
        DATA['array'].append(float(message.text))
        msg = bot.send_message(message.chat.id, '\U0001F60C Введите коэффицент Стьюдента:')
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
    #TODO: implement check input string
    msg = bot.send_message(message.chat.id, "Мне нужно знать ваше количество измерений\U0001F60C", reply_markup=get_keyboard())
    bot.register_next_step_handler(msg, count_step)

if __name__ == '__main__':
    bot.polling()
