#!/usr/bin/python3

import telebot
import time
import config
import calc

TOKEN = config.get_token()

bot = telebot.TeleBot(TOKEN)

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
    #TODO: implement input/output results from calc.py
    msg = bot.send_message(message.chat.id,'Welcom for calc!')

if __name__ == '__main__':
    print('Start')
    data = {
        'array' : [2,3,3,2],
        'count' : 4,
        'st' : 2.20,
        'error_device' : {'max_x' : 0.001}, # or 'error_device' : 0.01
        'error_round' : [0.1,10], #p = интервал = 0.1 ; h =цена деления = 10
        }
    c = calc.Calculator(data)
    print(c.get_small_result())
    print(c.get_detail_result())
