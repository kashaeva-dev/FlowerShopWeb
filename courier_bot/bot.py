import telebot
from django.conf import settings
from account.models import Staff

courier_id = settings.COURIER_TG_ID
telegrambot_token = settings.TELEGRAMBOT_TOKEN

bot = telebot.TeleBot(telegrambot_token)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id,
                     "В этот чат будут приходить новые заказы")


def send_order(order):
    curriers = Staff.objects.filter(role='currier')
    for currier in curriers:
        if order.currier == currier:
            bot.send_message(currier.tg_id, f'''Новый заказ:
                            ФИО: {order.contact_name}
                            Телефон: {order.contact_phone}
                            Букет: {order.bouquet.name}
                            Тип оплаты: {order.payment_type}''')


def run_courier_bot():
    bot.polling(none_stop=True, interval=0)
