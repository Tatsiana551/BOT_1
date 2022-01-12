import telebot
from telebot import types
import const


bot = telebot.TeleBot(const.API_TOKEN)


# объект клавиатуры (кнопки), в одной строке одна кнопка
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

# запросит текущую локацию
btn_adress = types.KeyboardButton('Адрес магазина', request_location=True)
btn_payment = types.KeyboardButton('Способы оплаты')
btn_delivery = types.KeyboardButton('Способы доставки')
btn_catalog = types.KeyboardButton('Каталог')
btn_baskets = types.KeyboardButton('Корзина')

# добавляем кнопки клавиатуры
markup_menu.add(btn_adress, btn_payment, btn_delivery, btn_catalog, btn_baskets)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Наличные', callback_data='cash')
btn_in_card = types.InlineKeyboardButton('По карте', callback_data='card')
markup_inline_payment.add(btn_in_cash, btn_in_card)

markup_inline_delivery = types.InlineKeyboardMarkup()
btn_in_courier = types.InlineKeyboardButton('Курьером', callback_data='courier')
btn_in_pickup = types.InlineKeyboardButton('Самовывоз', callback_data='pickup')
markup_inline_delivery.add(btn_in_courier, btn_in_pickup)

markup_inline_catalog = types.InlineKeyboardMarkup()
btn_in_flowers = types.InlineKeyboardButton('Хочу купить цветы', callback_data='flowers')
compositions_btn = types.InlineKeyboardButton("Хочу купить композицию", callback_data='compositions')
markup_inline_catalog.add(btn_in_flowers, compositions_btn)


@bot.message_handler(commands=['start','help'])
def send_wellcome(message):
    bot.reply_to(message, 'Привет, я бот цветочный магазин', reply_markup=markup_menu)

# @bot.message_handler(func=lambda message: True)
# def catalog_shop(message):
@bot.message_handler(func=lambda message: True)
def elho_all(message):
    if message.text == 'Способы доставки':
        bot.reply_to(message, 'Доставка', reply_markup=markup_inline_delivery)
    if message.text == 'Способы оплаты':
        bot.reply_to(message, 'В нашем магазине доступны следующие методы оплаты', reply_markup=markup_inline_payment)
    if message.text == 'Каталог':
        bot.reply_to(message, 'В продаже имеются следующие композиции цветов', reply_markup=markup_inline_catalog)
        # bot.reply_to(message,message.text, reply_markup=markup_menu)

@bot.callback_query_handler(func=lambda call: True)
def call_back_payment(call):
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text='''
        Наличная оплата производится в рублях''', reply_markup=markup_inline_payment)


# обрабатываем локацию
@bot.message_handler(func=lambda message: True, content_types=['location'])
def magazin_location(message):
    # получаем от пользователя координаты
    lon = message.location.longitude
    lat = message.location.latitude
    print(f'Широта(), долгота()', {lon,lat})



@bot.callback_query_handler(func=lambda call: True)
def callback_catalog(call):
    keyboard = create_keyboard()
    if call.message:
        if call.data == "flowers":
            img = open('bot_1/images (11).jpg', 'rb')
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=img,
                caption="Вдохновение",
                reply_markup=keyboard)
            img.close()
        if call.data == "compositions":
            img = open('bot_1/Без названия.jpg', 'rb')
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=img,
                caption="Для тебя",
                reply_markup=keyboard)
            img.close()


# SelectedCartId=0
# def GetCart(message):
#     markup=types.InlineKeyboardMarkup(row_width=2)
#     markup.add(
#         types.InlineKeyboardButton('<=====Back items', callback_data='BackCard'),
#         types.InlineKeyboardButton('Next item ===>', callback_data='NextCard'),
#     )
#     bot.send_photo(message.chat.id, open(f'const.items[SelectedCardId][0]','rb'), caption=f'''
#     Наименование: <b>{const.items[SelectedCardId][1]}<b>
#     Код: <b>{const.items[SelectedCartId][2]} RUR<b>
#     ''', parse_mode='html', reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     global SelectedCartId
#
#     if call_data == 'NextCard':
#
#         if SelectedCartId == len(const.items):
#             return bot.send_message(call.message.chat.id, 'Это последний товар')
#         else:
#             SelectedCartId +=1
#             GetCart(call.message)
#     elif call.data == 'BackCard':
#
#         if SelectedCartId ==1:
#             return bot.send_message(call.message.chat.id, 'Это последний товар')
#         else:
#             SelectedCartId -=1
#             GetCart(call.message)


bot.polling()