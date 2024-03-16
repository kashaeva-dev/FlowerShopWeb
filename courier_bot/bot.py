import telebot
from django.conf import settings
from flower_shop.models import Courier

courier_id = settings.COURIER_TG_ID
telegrambot_token = settings.TELEGRAMBOT_TOKEN

bot = telebot.TeleBot(telegrambot_token)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id,
                     "В этот чат будут приходить новые заказы")


def send_order(instance):
    couriers = Courier.objects.all()
    for courier in couriers:
        bot.send_message(courier.tg_id, f'''Новый заказ:
                        ФИО: {instance.contact_name}
                        Телефон: {instance.contact_phone}
                        Букет: {instance.bouquet.name}
                        Тип оплаты: {instance.payment_type}''')


def run_courier_bot():
    bot.polling(none_stop=True, interval=0)
