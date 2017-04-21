#!/usr/bin/python3

import telebot
import time
#TODO: import calc.py

TOKEN = '312970227:AAFnLLkMcJRENTQXOj3QTHEAqCLVgbgwx3c'

bot = telebot.TeleBot(TOKEN)

start_text = open('start_message.txt','r')
help_text = open('help_message.txt','r')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    out = start_text.read()
    msg = bot.send_message(message.chat.id, out)

@bot.message_handler(commands=['help'])
def help_message(message):
    out = help_text.read()
    msg = bot.send_message(message.chat.id, out)

@bot.message_handler(commands=['calc'])
def calc_operations(message):
    #TODO: implement input/output results from calc.py
    msg = bot.send_message(message.chat.id,'Welcom for calc!')

if __name__ == '__main__':
    bot.polling()
