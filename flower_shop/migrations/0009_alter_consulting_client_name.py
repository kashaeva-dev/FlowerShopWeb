# Generated by Django 5.0.3 on 2024-03-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower_shop', '0008_rename_created_at_consultingstatushistory_status_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulting',
            name='client_name',
            field=models.CharField(max_length=100, verbose_name='Имя клиента'),
        ),
    ]