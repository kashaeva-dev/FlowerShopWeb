from django.db import models
from django.conf import settings

class Staff(models.Model):
    STAFF_ROLE_CHOICES = (
        ('admin', 'Админ'),
        ('florist', 'Флорист'),
        ('currier', 'Курьер'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    role = models.CharField(max_length=40, verbose_name='Роль', choices=STAFF_ROLE_CHOICES)
    start_date = models.DateTimeField(verbose_name='Дата начала работы', auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='Дата увольнения', null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.role}'
