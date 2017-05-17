#!/usr/bin/python3


def get_token():
    return '312970227:AAFnLLkMcJRENTQXOj3QTHEAqCLVgbgwx3c'

def get_help():
    return '\U00002753 Почему не принимает значения?\n\U00002714 Проверьте корректность. Дробные(нецелые) значения должны быть только числами и разделяться точкой.\n\U00002753 Происходит ли округление результата?\n\U00002714 Да. В краткой форме до 3 знака, в подробной до 5.\n\U00002753 "Произошла ошибка в вычислениях", но я в ввёл всё правильно!\n\U00002714 Перепроверьте все коэффиценты и измерения. В большинстве случаев происходит деление на 0.\n\U00002753 "Подождите 1 минуту..."\n\U00002714 Из-за криворукости разработчика, я могу считать значения только одного человека, а остальные находятся в очереди.\n\U00002764 Если у вас остались вопросы или пожелания к проекту, то Вы всегда можете связаться с нами: feedbackservice.a@gmail.com'
def get_start():
    return ["Привет! Я помогу тебе с вычислениями. Я очень удобен и прост.\n\U00002757 Главные команды:\n\U00002714 /calc - расчет измерений\n\U00002714 /theory - теория расчета\n\U00002714 /help - помощь",
            "Доброй пожаловать! Я помогу тебе с вычислениями. Просто выбери нужную команду:\n\U00002714 /calc - расчет измерений\n\U00002714 /theory - теория расчета\n\U00002714 /help - помощь",
            "Здравствуйте! Я помогу Вам с вычислениями. Выберите необходимую команду:\n\U00002714 /calc - расчет измерений\n\U00002714 /theory - теория расчета\n\U00002714 /help - помощь",
            ]
def unittest():
    print(get_help())
    print(get_start())

if __name__ == '__main__':
    unittest()
