#!/usr/bin/python3


def get_token():
    return '312970227:AAFnLLkMcJRENTQXOj3QTHEAqCLVgbgwx3c'

def get_help():
    return """Что-то не понятно? Всё просто:
            введи  количество измерений.
            """
def get_start():
    return """Привет! Я помогу тебе с вычислениями!
            Для начала я хочу знать сколько ты сделал измерений?
            Подробная информация по команде /help.
            """
def unittest():
    print(get_help())
    print(get_start())

if __name__ == '__main__':
    unittest()
