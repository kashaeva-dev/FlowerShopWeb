import telebot
from django.conf import settings

telegrambot_token = settings.TELEGRAMBOT_TOKEN

bot = telebot.TeleBot(telegrambot_token)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id,
                     "В этот чат будут приходить новые заказы")


def send_order(order):
    currier = order.currier
    if currier:
        bot.send_message(currier.tg_id, f'''Новый заказ:
                        ФИО: {order.contact_name}
                        Телефон: {order.contact_phone}
                        Букет: {order.bouquet.name}
                        Тип оплаты: {order.payment_type}''')


def run_courier_bot():
    bot.polling(none_stop=True, interval=0)
