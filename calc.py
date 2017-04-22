#!/usr/bin/python3

import math

class Calculator():
    def __init__(self,data):
        self.result = dict()
        self.setup(data)

    #TODO: in process...

    def get_small_result(self):
        'получение результата'
        self.calc()
        e = round(self.result['eps_error'],3)
        x = round(self.result['average_summ'],3)
        delt_x = round(self.result['full_error'],3)
        return [x,delt_x,e]

    def get_detail_result(self):
        return self.result

    def setup(self,data):
        'quick setup settings'
        self.storage = data['array']
        self.count = data['count']
        self.error_device = 0.0067
        self.error_round = 0.0048
        #TODO:implements correct data
        #self.error_device = data['error_device']
        #self.error_round = data['error_round']
        self.st = data['st']

    def calc(self):
        self.push_average_summ()
        self.push_rand_error(self.result['average_summ'],
                            self.count)
        self.push_qtrs(self.result['rand_error'])
        self.push_average_qtr(self.result['qtrs'])
        self.push_all_average(self.result['average_qtr'])
        self.push_random_error(self.result['all_average'])

        self.push_full_error(self.result['random_error'],self.error_device,self.error_round)

        self.push_eps_error(self.result['full_error'],
                            self.result['average_summ'])


    def set_array(self,count):
        'задать массив-измерений'
        for i in range(0,):
            data = float(input('| X['+str(i+1)+'] =  '))
            self.storage.append(data)

    def set_count(self,value):
        'задать кол-в измерений' #TODO count ?= len(array)?
        self.count = value

    def set_error_device(self,value = 0.0067):
        'задать ошибку прибора'
        self.error_device = value

    def set_error_round(self,value = 0.0048):
        'задать ошибку округления'
        self.error_round = value

    def push_average_summ(self):
        'Среднее арифметическое'
        average_summ = 0
        for i in range(0,self.count):
            average_summ += self.storage[i]
        average_summ = average_summ / self.count
        self.result['average_summ'] = average_summ

    def push_rand_error(self,average_summ,count):
        'Cлучайная погрешность для каждого измерения'
        rand_error = []
        for i in range(0,count):
            rand_error.append(average_summ-self.storage[i])
        self.result['rand_error'] = rand_error

    def push_qtrs(self,rand_error):
        'Квадраты погрешностей'
        qtr = []
        for i in rand_error:
            qtr.append(i**2)
        self.result['qtrs'] = qtr

    def push_average_qtr(self,qtr):
        'Средняя квадратичная погрешнoсть'
        temp_sum = 0
        for elem in qtr:
            temp_sum += elem;
        temp_sum = temp_sum / (self.count - 1)
        average_qtr = math.sqrt(temp_sum)
        self.result['average_qtr'] = average_qtr

    def push_all_average(self,average_qtr):
        'Средняя квадртичная погрешность всего результата'
        all_average = average_qtr / self.count*(self.count-1)
        self.result['all_average'] = all_average

    def push_random_error(self,all_average):
        random_error = self.st * all_average
        self.result['random_error'] = random_error

    def push_full_error(self,random_error,error_device,error_round):
        'Полная абсолютная погрешность'
        full_error = random_error*random_error + error_device*error_device + error_round*error_round
        self.result['full_error'] = math.sqrt(full_error)

    def push_eps_error(self,full_error,average_summ):
        'Относительная погрешность результата'
        eps_error = full_error / average_summ * 100
        self.result['eps_error'] = eps_error

def test():
    print('unittests...')
    #create test data
    data = {
        'array' : [2,3,3,2],
        'count' : 4,
        'st' : 2.20,
        'error_device' : {'max_x' : 0.001}, # or 'error_device' : 0.01
        'error_round' : [0.1,10], #p = интервал = 0.1 ; h =цена деления = 10
        }
    C = Calculator(data)
    if (C.storage != data['array']) and (len(C.array) != data['count']):
        print('Error set array..')
    else:
        if C.st != data['st']:
            print('Error set coeff. student')
        else:
            print('successfull!')

if __name__ == '__main__':
    test()
