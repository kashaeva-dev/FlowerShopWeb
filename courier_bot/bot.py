from django.dispatch import receiver
from django.db.models.signals import post_save
import telebot
from django.conf import settings

courier_id = settings.COURIER_TG_ID 
telegrambot_token = settings.TELEGRAMBOT_TOKEN

bot = telebot.TeleBot(telegrambot_token)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(courier_id, "В этот чат будут приходить новые заказы")


def send_order(instance):
    bot.send_message(courier_id, f"Новый заказ:\nФИО: {instance.contact_name}\nТелефон: {instance.contact_phone}\nБукет: {instance.bouquet.name}\nТип оплаты: {instance.payment_type}")


def run_courier_bot():
    bot.polling(none_stop=True, interval=0)