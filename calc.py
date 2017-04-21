#!/usr/bin/python3

import math

class Calculator()
    def __init__(data):
        self.array = data['array']
        self.count = data['count']
        self.st = data['st']
        #TODO: change
        self.error_device = 0.0067
        self.error_round = 0.0048
        self.results = []

    #TODO: in process...
    def get_result():
        'получение результата'
        pass
    def set_array():
        'задать массив-измерений'
        pass
    def set_count():
        'задать кол-в измерений' #TODO count ?= len(array)?
        pass
    def set_error_device():
        'задать ошибку прибора'
        pass
    def set_error_round():
        'задать ошибку округления'
        pass

    def push_average_summ():
        'Среднее арифметическое'
        average_summ = 0
        for i in range(0,self.count):
            average_summ += self.array[i]
        average_summ = average_summ / self.count
        self.result.update(['average_summ',average_summ])

    def push_rand_error(average_summ):
        'Cлучайная погрешность для каждого измерения'
        rand_error = []
        for i in range(0,COUNT):
            rand_error.append(average_summ-self.array[i])
        self.result.update(['rand_error',rand_error])

    def push_qtrs(rand_error):
        'Квадраты погрешностей'
        qtr = []
        for i in rand_error:
            qtr.append(rand_error**2)
        self.result.update(['qtrs',qtr])

    def push_average_qtr(qtr):
        'Средняя квадратичная погрешнoсть'
        temp_sum = 0
        for elem in qtr:
            temp_sum += elem;
        temp_sum = temp_sum / (COUNT - 1)
        average_qtr = math.sqrt(temp_sum)
        self.results.update(['average_qtr',average_qtr])

    def push_all_average(average_qtr):
        'Средняя квадртичная погрешность всего результата'
        all_average = average_qtr / self.count*(self.count-1)
        self.results.update(['all_average',all_average])
    def push_random_error(all_average):
        random_error = self.st * all_average
        self.results.update(['random_error',random_error])

    def push_full_error(random_error,error_device,error_round):
        'Полная абсолютная погрешность'
        full_error = random_error**2 + error_device**2 + error_round**2
        self.results.update(['full_error',math.sqrt(full_error)])

    def push_eps_error(full_error,average_summ):
        'Относительная погрешность результата'
        eps_error = full_error / average_summ * 100
        self.results.update(['eps_error',eps_error])

def test():
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
    C = Calculator(data)
    #TODO: implements test for class!!!

if __name__ == '__main__':
    test()
