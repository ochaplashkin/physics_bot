#!/usr/bin/python3

# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import config
import calc
import random

#TODO:implements connect logging and out debug strings
#import logging

TOKEN = config.get_token()

bot = telebot.TeleBot(TOKEN)

DATA = {}

CMDS = {'/help','/start','/calc','/theory','Помощь','Теория расчётов','Расчёт',
        'помощь','теория расчётов','расчёт','домой','теория расчетов','расчет',
        'Домой','Дом','Меню','меню','help','start','go','calc','theory','home',
        'menu','Menu'
        }

def safely_convert(text,variant='float'):
    if variant == 'float':
        try:
            return [0,float(text)]
        except:
            return [1]
    else:
        try:
            return [0,int(text)]
        except:
            return [1]

def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    markup.row('Расчет','Теория расчета')
    markup.row('Помощь')
    return markup

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
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        try:
            result = calc.Calculator(DATA)
            result.set_error_device(DATA['error_device'])
            x = result.get_small_result()[0]
            delt_x = result.get_small_result()[1]
            eps = result.get_small_result()[2]
            if message.text == 'Коротко':
                out_string = '\U000025B6 Результат:\n\U000025FB x = {0} +/- {1}\n'.format(x,delt_x)
                out_string += '\U000025B6 Относительная погрешность:\n\U000025FB{}\n'.format(eps)
                msg = bot.send_message(message.chat.id,out_string,reply_markup=menu_keyboard())
                bot.register_next_step_handler(msg,branching)
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
                msg = bot.send_message(message.chat.id,out_string,reply_markup=menu_keyboard())
                bot.register_next_step_handler(message,branching)
        except:
            msg = bot.send_message(message.chat.id,'\U00002757Проверьте входные параметры! Произошла ошибка в вычислениях.\n\U00002714 /help - помощь',reply_markup=menu_keyboard())
            bot.register_next_step_handler(msg,branching)


def input_error_round(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        msg_to_numb = safely_convert(message.text,'float')
        if msg_to_numb[0] == 0:
            DATA['error_round'] = msg_to_numb[1]
            msg = bot.send_message(message.chat.id, 'Готово! В какой форме вам нужен результат?', reply_markup = result_key())
            bot.register_next_step_handler(msg,select_result)
        else:
            msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..')
            bot.register_next_step_handler(msg, input_error_round)

def helper_h(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        msg_to_numb = safely_convert(message.text,'float')
        if msg_to_numb[0] == 0:
            DATA['error_device']['h'] = msg_to_numb[1]
            msg = bot.send_message(message.chat.id, 'И последнее - ошибка округления.')
            bot.register_next_step_handler(msg,input_error_round)
        else:
            msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..')
            bot.register_next_step_handler(msg, helper_p)

def helper_p(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        msg_to_numb = safely_convert(message.text,'float')
        if msg_to_numb[0] == 0:
            DATA['error_device'] = {}
            DATA['error_device']['p'] = msg_to_numb[1]
            msg = bot.send_message(message.chat.id, 'Цена деления прибора:')
            bot.register_next_step_handler(msg,helper_h)
        else:
            msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..')
            bot.register_next_step_handler(msg, helper_p)

def helper_err(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        msg_to_numb = safely_convert(message.text,'float')
        if msg_to_numb[0] == 0:
            DATA['error_device'] = msg_to_numb[1]
            msg = bot.send_message(message.chat.id, 'И последнее - ошибка округления.')
            bot.register_next_step_handler(msg,input_error_round)
        else:
            msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..')
            bot.register_next_step_handler(msg, helper_err)


def input_error_device(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        if message.text == 'Расчитать':
            msg = bot.send_message(message.chat.id, 'Интервал вероятности:')
            bot.register_next_step_handler(msg,helper_p)
        else:
            bot.send_message(message.chat.id,'Ожидаю...')
            bot.register_next_step_handler(message,helper_err)

def coeff(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        msg_to_numb = safely_convert(message.text,'float')
        if message.text != '/help_st':
            if msg_to_numb[0] == 0:
                DATA['st'] = msg_to_numb[1]
                msg = bot.send_message(message.chat.id, 'Еще немного. Введите ошибку прибора:',reply_markup=answer_key())
                bot.register_next_step_handler(msg,input_error_device)
            else:
                msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..')
                bot.register_next_step_handler(msg, coeff)
        else:
            #TODO: implements help for coeff st
            bot.register_next_step_handler(message,help_st)

def check_value(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        msg_to_numb = safely_convert(message.text,'float')
        if DATA['iter'] <= DATA['count']-1:
            if msg_to_numb[0] == 0:
                DATA['array'].append(msg_to_numb[1])
                DATA['iter'] += 1
                msg = bot.send_message(message.chat.id,'\U00002611 Значение №'+str(DATA['iter'])+':')
                bot.register_next_step_handler(msg,check_value)
            else:
                msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..')
                bot.register_next_step_handler(msg, check_value)
        else:
            if msg_to_numb[0] == 0:
                DATA['array'].append(msg_to_numb[1])
                msg = bot.send_message(message.chat.id, 'Введите коэффицент Стьюдента:\n\U00002753Не можете вспомнить?\n/help_st - уточните.')
                bot.register_next_step_handler(msg,coeff)
            else:
                msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..')
                bot.register_next_step_handler(msg, check_value)

def count_step(message):
    if message.text in CMDS:
        msg = bot.send_message(message.chat.id,'Переход в главное меню'.format(message.text),reply_markup=menu_keyboard())
        bot.register_next_step_handler(msg,branching)
    else:
        msg_to_numb = safely_convert(message.text,'int')
        if msg_to_numb[0] == 0:
            DATA['count'] = msg_to_numb[1]
            msg = bot.send_message(message.chat.id, 'Отлично! Необходимы ваши измерения.\n\U00002611 Значение №{}:'.format(DATA['iter']))
            bot.register_next_step_handler(msg,check_value)
        else:
            msg = bot.send_message(message.chat.id, 'Нет, нет\U0001F612 Я жду от Вас число..', reply_markup = get_keyboard())
            bot.register_next_step_handler(msg, count_step)

def branching(message):
    print('branch',message.text)
    if message.text == 'Расчет':
        calc_operations(message)
    if message.text == 'Теория расчета':
        theory_message(message)
    if message.text == 'Помощь':
        help_message(message)

@bot.message_handler(commands=['theory'])
def theory_message(message):
    msg = bot.send_message(message.chat.id,'Теория пишется...',reply_markup=menu_keyboard())
    bot.register_next_step_handler(msg, branching)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    to = len(config.get_start())
    i = random.randint(0,2)
    out = config.get_start()[i]
    msg = bot.send_message(message.chat.id, out,reply_markup = menu_keyboard())
    bot.register_next_step_handler(msg, branching )

@bot.message_handler(commands=['help','помощь'])
def help_message(message):
    out = config.get_help()
    msg = bot.send_message(message.chat.id, out,reply_markup = menu_keyboard())
    bot.register_next_step_handler(msg, branching )

@bot.message_handler(commands=['/help_st'])
def help_st(message):
    msg = bot.send_message(message.chat.id, 'Я в хелпере стьюдента!')

@bot.message_handler(commands=['calc'])
def calc_operations(message):
    DATA['array'] = []
    DATA['iter'] = 1
    msg = bot.send_message(message.chat.id, "Мне нужно знать ваше количество измерений", reply_markup=get_keyboard())
    bot.register_next_step_handler(msg, count_step)

if __name__ == '__main__':
    bot.polling(none_stop=True)
