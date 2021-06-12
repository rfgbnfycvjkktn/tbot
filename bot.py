# -*- coding: utf-8 -*-
import re
import datetime
import telebot
from telebot import types
from keyboards import InlineKeyboard
from dotenv import load_dotenv
import os

import bonds

import prettytable as pt

from telebot import types

import users

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

provider_token = '381764678:TEST:26515'
prices = [types.LabeledPrice(label='Подписка', amount=10000)]
param = {'yieldless': 0, 'yieldmore': 0, 'priceless': 0, 'pricemore': 0, 'durationless': 0, 'durationmore': 0,
         'volume': 0}


# стартовая страница обработка команды
@bot.callback_query_handler(func=lambda query: query.data == 'start')
def callback_inline(call):
    buttons = {'search_main_page': u'\U0001F50D' + ' Поиск', 'buy': u'\U0001F4B3' + ' Подписка',
               'help': u'\U00002139' + ' Помощь'}
    InlineKeyboard.callback_keyboard(call.message, buttons,
                                     u'\U00002705' + '<b>Умный рантье (поиск облигации)</b> - сервис подбора '
                                                     'ликвидных облигаций. Бот предоставляет обработанную для '
                                                     'пользователя информацию с серверов Московской биржи.' + '\n' +
                                     u'\U00002757' + 'Бот предоставляет информацию на основе данных '
                                                     'последней завершенной торговой сессии (НЕ текущий день).' + '\n' +
                                     u'\U00002757' + '<b>Важно.</b> Информация, полученная с помощью данного сервиса,'
                                                     'не является индивидуальной рекомендацией; носит исключительно '
                                                     ' информационно-аналитический '
                                                     'характер и не должна рассматриваться как предложение либо '
                                                     'рекомендация к инвестированию, покупке, продаже какого-либо '
                                                     'актива, торговых операций по финансовым инструментам.')

    user = users.User()
    data = {'ID': call.from_user.id,
            'Name': call.from_user.first_name,
            'access': False,
            'reg_date': datetime.datetime.today().replace(microsecond=0),
            'sub_start_date': None,
            'sub_end_date': None}
    user.add(data)


# стартовая страница через коллбек
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.clear_step_handler(message)
    buttons = {'search_main_page': u'\U0001F50D' + ' Поиск', 'buy': u'\U0001F4B3' + ' Подписка',
               'help': u'\U00002139' + ' Помощь'}
    InlineKeyboard.callback_keyboard(message, buttons,
                                     u'\U00002705' + '<b>Умный рантье (поиск облигации)</b> - сервис подбора '
                                                     'ликвидных облигаций. Бот предоставляет обработанную для '
                                                     'пользователя информацию с серверов Московской биржи.' + '\n' +
                                     u'\U00002757' + 'Бот предоставляет информацию на основе данных '
                                                     'последней завершенной торговой сессии (НЕ текущий день).' + '\n' +
                                     u'\U00002757' + '<b>Важно.</b> Информация, полученная с помощью данного сервиса,'
                                                     'не является индивидуальной рекомендацией; носит исключительно '
                                                     ' информационно-аналитический '
                                                     'характер и не должна рассматриваться как предложение либо '
                                                     'рекомендация к инвестированию, покупке, продаже какого-либо '
                                                     'актива, торговых операций по финансовым инструментам.')

    # user = users.User()
    # data = {'ID': message.from_user.id,
    #         'Name': message.from_user.first_name,
    #         'access': False,
    #         'reg_date': datetime.datetime.today().replace(microsecond=0),
    #         'sub_start_date': None,
    #         'sub_end_date': None}
    # user.add(data)


# страница помощи обработка команды
@bot.message_handler(commands=["help"])
def start_command(call):
    buttons = {'start': u'\U00002B05' + ' На главную'}  # callback и наименоваине кнопки
    desc = '<b>Параметры, используемые при поиске:</b>' + '\n' + u'\U00000031' + u'\U000020E3' + ' Купонная доходность бумаги (% ' \
                                                                                                 'годовых). Основной параметр, ' \
                                                                                                 'от которого можно отталкиваться при ' \
                                                                                                 'принятии решения.' \
           + '\n' + u'\U00000032' + u'\U000020E3' + ' Цена (% от номинала). Рыночная цена в процентах от номинальной. ' \
                                                    'Обычно номинальная цена равна 1000 рублей (100 %) ' \
           + '\n' + u'\U00000033' + u'\U000020E3' + ' Дюрация (количество месяцев) — эффективный срок до погашения ' \
                                                    'облигации. Эффективный срок учитывает все купонные платежи, ' \
                                                    'выплаченные в разное время, и различные особенности облигации, ' \
                                                    'такие как амортизация или оферта. Если купонных платежей, ' \
                                                    'амортизации и оферты нет, то дюрация совпадает со сроком до ' \
                                                    'погашения облигации. ' \
           + '\n' + u'\U00000034' + u'\U000020E3' + ' Объем торгов бумагой (количество штук). На данный момент ' \
                                                    'анализируются последние 2 недели торгов бумагой. ' \
           + '\n\n' + u'\U0001F4B3' + '<b>Расширенный поиск:</b>' \
           + '\n' + u'\U00000031' + u'\U000020E3' + 'В процессе...'

    InlineKeyboard.callback_keyboard(call, buttons, desc)


@bot.message_handler(commands=["buy"])
def start_command(call):
    bot.send_message(call.chat.id,
                     "На данный момент платежи в тестовом режиме."
                     " Для оплаты используйте данные тестовой карты:"
                     "\n 1111 1111 1111 1026, 12/22, CVC 000"
                     "\n\nОплачиваемый товар:", parse_mode='Markdown')

    bot.send_invoice(call.chat.id, title='Подписка (30 дней)',
                     description=' Подписка открывает доступ к расширенному поиску облигаций на 30 дней от даты оплаты.',
                     provider_token=provider_token,
                     currency='RUB',
                     photo_url='',
                     photo_height=None,  # !=0/None or picture won't be shown
                     photo_width=None,
                     photo_size=None,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     prices=prices,
                     start_parameter='subs',
                     invoice_payload='HAPPY FRIDAYS COUPON')


@bot.callback_query_handler(func=lambda query: query.data == 'buy')
def callback_inline(call):
    print('1')


# страница помощи
@bot.callback_query_handler(func=lambda query: query.data == 'help')
def callback_inline(call):
    buttons = {'start': u'\U00002B05' + ' На главную'}  # callback и наименоваине кнопки
    desc = '<b>Параметры, используемые при поиске:</b>' + '\n' + u'\U00000031' + u'\U000020E3' + ' Купонная доходность бумаги (% ' \
                                                                                                 'годовых). Основной параметр, ' \
                                                                                                 'от которого можно отталкиваться при ' \
                                                                                                 'принятии решения.' \
           + '\n' + u'\U00000032' + u'\U000020E3' + ' Цена (% от номинала). Рыночная цена в процентах от номинальной. ' \
                                                    'Обычно номинальная цена равна 1000 рублей (100 %) ' \
           + '\n' + u'\U00000033' + u'\U000020E3' + ' Дюрация (количество месяцев) — эффективный срок до погашения ' \
                                                    'облигации. Эффективный срок учитывает все купонные платежи, ' \
                                                    'выплаченные в разное время, и различные особенности облигации, ' \
                                                    'такие как амортизация или оферта. Если купонных платежей, ' \
                                                    'амортизации и оферты нет, то дюрация совпадает со сроком до ' \
                                                    'погашения облигации. ' \
           + '\n' + u'\U00000034' + u'\U000020E3' + ' Объем торгов бумагой (количество штук). На данный момент ' \
                                                    'анализируются последние 2 недели торгов бумагой. ' \
           + '\n\n' + u'\U0001F4B3' + '<b>Расширенный поиск:</b>' \
           + '\n' + u'\U00000031' + u'\U000020E3' + ' В разработке...'

    InlineKeyboard.callback_keyboard(call.message, buttons, desc)


@bot.callback_query_handler(func=lambda query: query.data == 'search_main_page')
def callback_inline(call):
    buttons = {'free_search_main_page': u'\U0001F50D' + ' Поиск',
               'pay_search_main_page': u'\U0001F50D' + ' Поиск (по подписке)',
               'start': u'\U00002B05' + ' На главную'}
    InlineKeyboard.callback_keyboard(call.message, buttons,
                                     '<b>Поиск облигаций.</b>' + '\n' + u'\U00002757 В <b>базовом</b> варианте поиск осуществляется по ограниченному '
                                                                        'набору параметров. Доходность бумаг от 4 до 8 процентов. Цена - 98 - 100 '
                                                                        'процентов от номинала. Значение объема сделок по бумаге предопределено и равно '
                                                                        'более 2500 штук за последние 2 недели ' + '\n' + u'\U00002757 Разработка <b>расширенного</b> функционала в процессе тестирования...')


# поиск по бесплатному тарифу
@bot.callback_query_handler(func=lambda query: query.data == 'free_search_main_page')
def callback_inline(call):
    buttons = {'yield_less_4': '4', 'yield_less_5': '5', 'yield_less_6': '6', 'yield_less_7': '7'}
    InlineKeyboard.callback_keyboard_one_row(call.message, buttons, 'Доходность от (%):')


# поиск по платному тарифу
@bot.callback_query_handler(func=lambda query: query.data == 'pay_search_main_page')
def callback_inline(message):
    bot.clear_step_handler(message.message)
    # msg = bot.reply_to(message.message, 'Доходность от:')
    # bot.edit_message_text(msg, message.chat.id, message.id, parse_mode='html', reply_markup=reply_markup)
    # msg = bot.edit_message_text('Доходность от:', message.message.chat.id, message.message.id, parse_mode='html')
    # keyboard = types.InlineKeyboardMarkup()
    # button = types.InlineKeyboardButton(text='Сброс', callback_data='pay_search_main_page')
    # keyboard.add(button)

    reply_markup = init_nav_button()

    msg = bot.send_message(message.message.chat.id, 'Доходность от (%):', reply_markup=reply_markup)
    bot.register_next_step_handler(msg, process_yield_less_step)


@bot.callback_query_handler(func=lambda c: True)
def callback_inline(callback):
    if re.match('yield_less_', callback.data):
        print("Выбрана доходность от")
        yieldless = callback.data.replace('yield_less_', "")
        param['yieldless'] = float(yieldless)

        # кнопки следующего меню
        buttons = {'yield_more_5': '5', 'yield_more_6': '6', 'yield_more_7': '7', 'yield_more_8': '8'}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons, 'Доходность до (%):')

    elif re.match('yield_more_', callback.data):
        print("Выбрана доходность до")
        yieldmore = callback.data.replace('yield_more_', "")
        param['yieldmore'] = float(yieldmore)

        # кнопки следующего меню
        buttons = {'price_less_98': '98', 'price_less_99': '99'}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons, 'Цена от (% от номинала):')

    elif re.match('price_less_', callback.data):
        print("Выбрана цена от")
        priceless = callback.data.replace('price_less_', "")
        param['priceless'] = float(priceless)

        # кнопки следующего меню
        buttons = {'price_more_99': '99', 'price_more_100': '100'}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons, 'Цена до (% от номинала):')

    elif re.match('price_more_', callback.data):
        print("Выбрана цена до")
        pricemore = callback.data.replace('price_more_', "")
        param['pricemore'] = float(pricemore)

        # все параметры бесплатного тарифа выбраны/установлены. Нужно произвести расчет
        param['volume'] = 2500

        param['durationless'] = 4
        param['durationmore'] = 36

        bot.send_chat_action(callback.message.chat.id, 'typing', 10)

        buttons = {}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons,
                                                 '<b>Параметры поиска:</b> \n' + 'Доходность от ' + str(
                                                     param['yieldless']) + ' до ' + str(
                                                     param['yieldmore']) + '\n' + 'Цена от ' + str(
                                                     param['priceless']) + ' до ' + str(
                                                     param['pricemore']) + '\n' + 'Дюрация от ' + str(
                                                     param['durationless']) + ' до ' + str(
                                                     param['durationmore']) + '\n' + 'Объем торгов от ' + str(
                                                     param['volume']))
        start_request(callback.message, False)


def start_request(message, paid=False):
    out_result = bonds.get_bonds(param)
    # получили данные

    if paid:
        table = pt.PrettyTable(['ИД', 'Наименование', 'Цена', 'Доход', 'Объём', 'Д-я'])
        table.align['Д-я'] = 'c'
    else:
        table = pt.PrettyTable(['ИД', 'Наименование', 'Цена', 'Доход', 'Объём'])

    table.align['ИД'] = 'l'
    table.align['Наименование'] = 'l'
    table.align['Цена'] = 'c'
    table.align['Доход'] = 'c'
    table.align['Объём'] = 'c'

    for bond in out_result:
        name = bond[1][0:20]
        if paid:
            table.add_row([bond[0], name, bond[2], bond[3], bond[4], bond[5]])
        else:
            table.add_row([bond[0], name, bond[2], bond[3], bond[4]])

    buttons = {'start': u'\U00002B05' + ' На главную'}
    InlineKeyboard.callback_keyboard(message, buttons, '<b>Результаты поиска</b> \n' + f'<pre>{table}</pre>')


def process_yield_less_step(message):
    reply_markup = init_nav_button()
    try:
        param['yieldless'] = float(message.text)
        # msg = bot.reply_to(message, 'Доходность до:')
        # msg = bot.edit_message_text('Доходность до:', message.chat.id, message.id, parse_mode='html')
        msg = bot.send_message(message.chat.id, 'Доходность до (%):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_yield_more_step)

    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_yield_more_step(message):
    reply_markup = init_nav_button()
    try:
        param['yieldmore'] = float(message.text)
        # msg = bot.reply_to(message, 'Цена от:')
        # msg = bot.edit_message_text('Цена от:', message.chat.id, message.id, parse_mode='html')
        msg = bot.send_message(message.chat.id, 'Цена от (% от номинала):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_price_less_step)
    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_price_less_step(message):
    reply_markup = init_nav_button()
    try:
        param['priceless'] = float(message.text)
        # msg = bot.reply_to(message, 'Цена до:')
        # msg = bot.edit_message_text('Цена до:', message.chat.id, message.id, parse_mode='html')
        reply_markup = init_nav_button()
        msg = bot.send_message(message.chat.id, 'Цена до (% от номинала):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_price_more_step)
    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_price_more_step(message):
    reply_markup = init_nav_button()
    try:
        param['pricemore'] = float(message.text)
        # msg = bot.reply_to(message, 'Дюрация от:')
        # msg = bot.edit_message_text('Дюрация от:', message.chat.id, message.id, parse_mode='html')
        msg = bot.send_message(message.chat.id, 'Дюрация от (мес.):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_duration_less_step)
    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_duration_less_step(message):
    reply_markup = init_nav_button()
    try:
        param['durationless'] = float(message.text)
        # msg = bot.reply_to(message, 'Дюрация до:')
        # msg = bot.edit_message_text('Дюрация до:', message.chat.id, message.id, parse_mode='html')
        reply_markup = init_nav_button()
        msg = bot.send_message(message.chat.id, 'Дюрация до (мес.):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_duration_more_step)
    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_duration_more_step(message):
    reply_markup = init_nav_button()
    try:
        param['durationmore'] = float(message.text)
        # msg = bot.reply_to(message, 'Объём торгов от:')
        # msg = bot.edit_message_text('Объём торгов от:', message.chat.id, message.id, parse_mode='html')
        reply_markup = init_nav_button()
        msg = bot.send_message(message.chat.id, 'Объём торгов от (шт.):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_volume_step)
    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_volume_step(message):
    reply_markup = init_nav_button()
    # try:
    param['volume'] = int(message.text)

    bot.clear_step_handler(message)

    bot.send_message(message.chat.id,
                     '<b>Параметры поиска:</b> \n'
                     + 'Доходность от ' + str(param['yieldless']) + ' до ' + str(param['yieldmore'])
                     + '\n' + 'Цена от ' + str(param['priceless']) + ' до ' + str(param['pricemore'])
                     + '\n' + 'Дюрация от ' + str(param['durationless']) + ' до ' + str(param['durationmore'])
                     + '\n' + 'Объем торгов от ' + str(param['volume'])
                     + '\n', parse_mode='html')

    start_request(message, True)

    # except Exception as e:
    #     bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()


def init_nav_button():
    keyboard = [
        [
            types.InlineKeyboardButton(u'\U00002B05' + ' На главную', callback_data='start'),
            types.InlineKeyboardButton(u'\U0000267B' + ' Сброс', callback_data='pay_search_main_page'),
        ]
    ]

    return types.InlineKeyboardMarkup(keyboard)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="В процессе оплаты возникли ошибки. Повторите оплату позже.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Поздравляю! Подписка активирована. Проверить статус можно командой \/sub'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


bot.polling()
