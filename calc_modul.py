#!/usr/bin/python3

# -*- coding: utf-8 -*-

import math
import sys
import main_window

def get_error_device(value):
    if type(value['error_device']) == dict:
        return  value['st']*value['error_device']['max_x']/2
    else:
        return value['error_device']

def get_error_round(value):
    if type(value['error_round']) == list:
        return value['error_round'][0]*value['error_round'][1]/2
    else:
        return value['error_round']

def calculate(data):
    f = open('out_results.txt','w')

    ARRAY = data['array']
    COUNT = data['count']
    ST = data['st']
    ERROR_DEVICE = 0.0067
    ERROR_ROUND = 0.0048

    f.write('Последовательные результаты вычислений \n')
    average_summ = 0
    for i in range(0,COUNT):
        average_summ += ARRAY[i]
    average_summ = average_summ / COUNT
    f.write('Среднее арифметическое = '+ str(average_summ)+'\n')

    rand_error = []
    for i in range(0,COUNT):
        rand_error.append(average_summ-ARRAY[i])
    f.write('Случайная погрешость для каждого: \n')
    s = 1
    for elem in rand_error:
        f.write('|X['+str(s)+'] =  |' + str(elem) + '|'+'\n')
        s +=1

    correct = 0;
    for elem in rand_error:
        correct += elem;
    f.write('Проверка корректности измерений: ' + str(correct) + '\n')

    qtr = []
    for elem in rand_error:
        qtr.append(elem*elem)

    f.write('Квадраты погрешностей: \n')
    s = 1
    for elem in qtr:
        f.write('|X['+str(s)+'] =  |' +str(elem) + '| \n')
        s +=1

    temp_sum = 0
    for elem in qtr:
        temp_sum += elem;
    temp_sum = temp_sum / (COUNT - 1)
    average_qtr = math.sqrt(temp_sum)
    f.write('Средняя квадратичная погрешность: '+str(average_qtr)+'\n')

    all_average = average_qtr / (COUNT*(COUNT-1))
    f.write('Средняя квадратичная погрешность всего результата: '+str(all_average) +'\n')

    random_error = ST*all_average
    f.write('Случайная погрешность: ' + str(random_error) +'\n')
    f.write('Погрешность прибора : '+ str(ERROR_DEVICE) + '\n')

    f.write('Погрешность округления : '+ str(ERROR_ROUND) + '\n')



    full_error = random_error**2 + ERROR_DEVICE**2 + ERROR_ROUND**2
    full_error = math.sqrt(full_error)
    f.write('Полная абсолютная погрешность измерений: '+str(full_error) +'\n')

    eps_error = full_error / average_summ * 100
    f.write('Относительная погрешность результата: ' + str(eps_error) + '\n')
    f.write('\fРезультат: \n')
    f.write('x = '+str(average_summ)+'+/-'+str(full_error) +'\n')
    f.write('E = ' + str(eps_error) +'\n')

def main():
    print('\fРасчет погрешности измерений. \nПожалуйста, следуйте инструкциям.\f')
    COUNT = int(input('Введите количество измерений: '))
    print('Введите значение для каждого измерения:')
    ARRAY = []
    for i in range(0,COUNT):
        data = float(input('| X['+str(i+1)+'] =  '))
        ARRAY.append(data)
    print('\fТаблица входных значений:')

    k = 1
    for e in ARRAY:
        print('| X['+str(k)+'] = '+str(e))
        k +=1
    ST = float(input('\fВведите коэффицент Стьюдента:'))
    data = {
        'array' : ARRAY,
        'count' : COUNT,
        'st' : ST,
        'error_device' : {'max_x' : 0.001}, # or 'error_device' : 0.01
        'error_round' : [0.1,10], #p = интервал = 0.1 ; h =цена деления = 10
    }
    calculate(data)

if __name__ == '__main__':
    main()
