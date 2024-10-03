"""
Header: Проверка функциональности тестируемого приложения
"""

import pygats.pygats as pyg
import pygats.recog as rec
from pygats.formatters import MarkdownFormatter as MD
import subprocess
import time

# Контекст, содержащий форматтер, который описывает правила
ctx = pyg.Context(MD())


def setup(ctx):
    ctx.formatter.print_header(3, 'Подготовка стенда к работе')

    server = subprocess.Popen(['python3', '../app/app.py'])
    time.sleep(1)
    if server is None:
        pyg.failed(msg='Ошибка запуска сервера')

    browser = subprocess.Popen(['firefox', '--new-tab', 'http://localhost:5000'])
    time.sleep(1)
    if browser is None:
        pyg.failed(msg='Ошибка запуска firefox')
    print(browser.pid)

    pyg.passed(ctx)
    return server, browser


def teardown(ctx, server, browser):

    ctx.formatter.print_header(3, 'Завершение работы стенда')
    pyg.alt_with_key(ctx, 'F4')
    server.kill()
    browser.kill()
    pyg.passed(ctx)


def test_greeteng():
    """
    Definition: Проверка функциональности первой страницы
    Actions:
        1: Ввести имя в поле ввода
        2: Нажать кнопку и поздороваться

    Expected: на экране надпись "Привет, Тестировщик!
    """
    def action_write_in_form():
        rec.click_text(ctx, rec.SearchedText('Иван', 'rus', 'top-left'))
        pyg.typewrite(ctx, 'Тестировщик', 'rus')

    pyg.run_action(ctx, action_write_in_form)

    def action_hello():
        rec.click_text(ctx, rec.SearchedText('Поздороваться', 'rus', 'all'))
        rec.check_text_on_screen(ctx, rec.SearchedText('Привет,', 'rus', 'all'))

    pyg.run_action(ctx, action_hello)



def test_go_to_admin_panel():
    """
    Definition: эта функция перехода в панель администратора

    Actions:
        1: переход в панель администратора

    Expected: пользователь перешел в панель администратора
    """
    # проверить переход на 2 страницу 
    def come_to_admin():
        rec.click_text(ctx, rec.SearchedText('Перейти', 'rus', 'all'))
        rec.check_text_on_screen(ctx, rec.SearchedText('Форма', 'rus', 'all'))

    pyg.run_action(ctx, come_to_admin) 


def test_create_note():
    """
    Definition: эта функция, которая вбивает значения в формы

    Actions:
        1: Заполнить все формы
        2: Создать учетную запись
     
    Expected: учетная заипсь создалась "Успешно"
    """
  
    def forms():
        rec.click_text(ctx, rec.SearchedText('Имя', 'rus', 'all'))
        pyg.typewrite(ctx, 'Иван', 'rus')

        rec.click_text(ctx, rec.SearchedText('Фамилия', 'rus', 'all'))
        pyg.typewrite(ctx, 'Иванов', 'rus')

        rec.click_text(ctx, rec.SearchedText('Пользователь', 'rus', 'all'))
        pyg.typewrite(ctx, 'Tester', 'eng')

        rec.click_text(ctx, rec.SearchedText('Почта', 'rus', 'all'))
        pyg.typewrite(ctx, 'email', 'eng')

        rec.click_text(ctx, rec.SearchedText('Адрес', 'rus', 'all'))
        pyg.typewrite(ctx, 'Саров', 'rus')

        rec.click_text(ctx, rec.SearchedText('Страна', 'rus', 'all'))

        # Нажимаем соответствую клавишу на клавиатуре
        pyg.press(ctx, 'down')
        pyg.press(ctx, 'enter')
        
        rec.click_text(ctx, rec.SearchedText('Область', 'rus', 'all'))
        pyg.press(ctx, 'down')
        pyg.press(ctx, 'enter')
    pyg.run_action(ctx,forms)#  првоерить возможность создать новую запись


    def create_account():
        rec.click_text(ctx, rec.SearchedText('Создать', 'rus', 'all'))
        rec.check_text_on_screen(ctx, rec.SearchedText('Успешно', 'rus', 'all'))
    pyg.run_action(ctx,create_account)
    


test_suites = [
    test_greeteng,
    test_go_to_admin_panel,
    test_create_note
]


if __name__ == '__main__':
    server, browser = setup(ctx)
    time.sleep(8)
    pyg.run(ctx, test_suites)
    teardown(ctx, server, browser)
