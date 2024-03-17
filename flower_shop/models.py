from django.db import models
from account.models import Staff
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from courier_bot.bot import send_order


class Occasion(models.Model):
    name = models.CharField(max_length=40, verbose_name='Повод')

    class Meta:
        verbose_name = 'Повод'
        verbose_name_plural = 'Поводы'

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    image = models.ImageField(verbose_name='Изображение', upload_to='bouquets')
    name = models.CharField(max_length=40, verbose_name='Название букета')
    description = models.TextField(verbose_name='Описание')
    content = models.TextField(verbose_name='Состав')
    occasion = models.ManyToManyField(Occasion,
                                      verbose_name='Повод',
                                      related_name='bouquets',
                                      )
    is_recommended = models.BooleanField(verbose_name='Рекомендуемый', default=False)
    price = models.PositiveIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return self.name

    def get_orders(self):
        return self.orders.all().count()


class ConsultingStatus(models.Model):
    name = models.CharField(max_length=40, verbose_name='Статус')

    class Meta:
        verbose_name = 'Статус консультации'
        verbose_name_plural = 'Статусы консультаций'

    def __str__(self):
        return self.name


class Consulting(models.Model):
    florist = models.ForeignKey(Staff,
                                on_delete=models.PROTECT,
                                verbose_name='Флорист',
                                limit_choices_to={'role': 'florist'},
                                related_name='consultings',
                                null=True,
                                blank=True,
                                )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    contact_phone = PhoneNumberField(verbose_name='Контактный телефон')
    first_call_at = models.DateTimeField(verbose_name='Дата и время звонка', null=True, blank=True)
    occasion = models.ForeignKey(Occasion,
                                 on_delete=models.PROTECT,
                                 verbose_name='Повод',
                                 related_name='consultings',
                                 null=True,
                                 blank=True,
                                 )
    agreement = models.BooleanField(verbose_name='Согласие на обработку персональных данных', default=False)

    def current_status(self):
        return self.status_history.order_by(
            '-status_created_at').first().status.name if self.status_history.exists() else None

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return f'{self.pk}: {self.client_name} - {self.created_at.strftime("%d.%m.%Y %H:%M")} - {self.current_status()}'


class ConsultingStatusHistory(models.Model):
    consulting = models.ForeignKey(Consulting,
                                   on_delete=models.CASCADE,
                                   verbose_name='Консультация',
                                   related_name='status_history',
                                   )
    status = models.ForeignKey(ConsultingStatus,
                               on_delete=models.PROTECT,
                               verbose_name='Статус',
                               related_name='status_history',
                               )
    status_created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'История статусов консультации'
        verbose_name_plural = 'Истории статусов консультаций'

    def __str__(self):
        return f'{self.consulting}: {self.status}'


class PaymentType(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тип оплаты')

    class Meta:
        verbose_name = 'Тип оплаты'
        verbose_name_plural = 'Типы оплаты'

    def __str__(self):
        return self.name


class DeliveryInterval(models.Model):
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Интервал доставки'
        verbose_name_plural = 'Интервалы доставки'

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В работе'),
        ('ready', 'Готов'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    )
    bouquet = models.ForeignKey(Bouquet,
                                on_delete=models.PROTECT,
                                verbose_name='Букет',
                                related_name='orders',
                                )
    consultation = models.ForeignKey(Consulting,
                                     on_delete=models.PROTECT,
                                     verbose_name='Консультация',
                                     related_name='orders',
                                     null=True,
                                     blank=True,
                                     )
    status = models.CharField(max_length=40, verbose_name='Статус', choices=STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    delivery_date = models.DateField(verbose_name='Дата доставки', blank=True, null=True)
    ealiest_delivery = models.BooleanField(verbose_name='Ранняя доставка', default=False)
    delivery_interval = models.ForeignKey(DeliveryInterval,
                                          on_delete=models.PROTECT,
                                          verbose_name='Интервал доставки',
                                          related_name='orders',
                                          null=True,
                                          blank=True,
                                          )
    delivery_address = models.CharField(max_length=200, verbose_name='Адрес доставки')
    contact_phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    contact_name = models.CharField(max_length=40, verbose_name='Контактное лицо')
    currier = models.ForeignKey(Staff,
                                on_delete=models.PROTECT,
                                verbose_name='Курьер',
                                limit_choices_to={'role': 'currier'},
                                related_name='orders',
                                null=True,
                                blank=True,
                                )
    payment_type = models.ForeignKey(PaymentType,
                                     on_delete=models.PROTECT,
                                     verbose_name='Тип оплаты',
                                     related_name='orders',
                                     default=1,
                                     )
    is_paid = models.BooleanField(verbose_name='Оплачен', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.bouquet.name}: ' \
               f'по адресу: {self.delivery_address} - {self.status}'
               # f' {self.delivery_date.strftime("%d.%m.%Y %H:%M")}' \
               # f'по адресу: {self.delivery_address} - {self.status}'


@receiver(pre_save, sender=Order)
def handle_new_order(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Order.objects.get(pk=instance.pk)
        if old_instance.currier != instance.currier:
            send_order(instance)
