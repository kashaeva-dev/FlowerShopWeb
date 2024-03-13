from django.db import models
from account.models import Staff


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
    price = models.PositiveIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return self.name


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
                                )
    status = models.ManyToManyField(ConsultingStatus,
                                    through='ConsultingStatusHistory',
                                    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    contact_phone = models.CharField(max_length=40, verbose_name='Контактный телефон')
    first_call_at = models.DateTimeField(verbose_name='Дата и время звонка', null=True, blank=True)
    occasion = models.ForeignKey(Occasion,
                                 on_delete=models.PROTECT,
                                 verbose_name='Повод',
                                 related_name='consultings',
                                 )

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return f'{self.pk}: {self.florist} - {self.created_at}'


class ConsultingStatusHistory(models.Model):
    consulting = models.ForeignKey(Consulting,
                                   on_delete=models.PROTECT,
                                   verbose_name='Консультация',
                                   related_name='status_history',
                                   )
    status = models.ForeignKey(ConsultingStatus,
                               on_delete=models.PROTECT,
                               verbose_name='Статус',
                               related_name='status_history',
                               )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'История статусов консультации'
        verbose_name_plural = 'Истории статусов консультаций'

    def __str__(self):
        return f'{self.consulting}: {self.status}'


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
    delivery_date = models.DateTimeField(verbose_name='Дата доставки')
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

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.bouquet.name}: ' \
               f' {self.delivery_date.strftime("%d.%m.%Y %H:%M")}' \
               f'по адресу: {self.delivery_address} - {self.status}'
