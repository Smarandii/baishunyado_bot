from telebot import types
from modules.content import *


def one_button_keyboard(text, callback_line, url=None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text=text, callback_data=callback_line, url=url)
    keyboard.add(button)
    return keyboard


def keyboard_maker(number_of_buttons: int,
                   text_for_each_button: list,
                   callback_data: list,
                   url_for_each_button: list = None,
                   without_back_btn: bool = False):
    if url_for_each_button is None:
        url_for_each_button = [None, None, None, None]
    keyboard = types.InlineKeyboardMarkup()
    if number_of_buttons > 1:
        butt1 = types.InlineKeyboardButton(text=text_for_each_button[0],
                                           callback_data=callback_data[0],
                                           url=url_for_each_button[0])
        keyboard.add(butt1)
    if number_of_buttons >= 2:
        butt2 = types.InlineKeyboardButton(text=text_for_each_button[1],
                                           callback_data=callback_data[1],
                                           url=url_for_each_button[1])
        keyboard.add(butt2)
    if number_of_buttons >= 3:
        butt3 = types.InlineKeyboardButton(text=text_for_each_button[2],
                                           callback_data=callback_data[2],
                                           url=url_for_each_button[2])
        keyboard.add(butt3)
    if number_of_buttons >= 4:
        butt4 = types.InlineKeyboardButton(text=text_for_each_button[3],
                                           callback_data=callback_data[3],
                                           url=url_for_each_button[3])
        keyboard.add(butt4)
    if not without_back_btn:
        backbutton = types.InlineKeyboardButton(text="Начать сначала", callback_data="start_test")
        keyboard.add(backbutton)
    return keyboard


PREVIEW_BUTTON = one_button_keyboard(text='Заглянуть в 2d рай (神を見る)',
                                     callback_line='None',
                                     url='https://t.me/joinchat/AAAAAFSR44l0ZT78wiwIXw')

BUY_BUTTON = one_button_keyboard(text='Купить пропуск в 2d рай (天国)',
                                 callback_line='None',
                                 url=BUY_URL)

INFORMATION_KEYBOARD = keyboard_maker(3,
                                      ['Инструкция по покупке доступа', 'Правила предложки', 'Как работает партнёрка'],
                                      ['', '', '', ''],
                                      url_for_each_button=[
                                          BUY_INSTRUCTION_URL,
                                          RULES_URL,
                                          PARTNERSHIP_URL
                                      ],
                                      without_back_btn=True)

PERSONAL_CABINET_KEYBOARD = keyboard_maker(2,
                                           ['Вывести деньги с баланса бота', 'Обновить ♻'],
                                           ['None', 'refresh'],
                                           [WITHDRAWAL_URL, None],
                                           without_back_btn=True)

SUGGESTION_RULES_BUTTON = one_button_keyboard('Правила предложки', 'None', url=RULES_URL)
PARTNERSHIP_RULES_BUTTON = one_button_keyboard('Как работает партнёрка', 'None', url=PARTNERSHIP_URL)
