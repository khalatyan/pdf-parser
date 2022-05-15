# Generated by Django 4.0.4 on 2022-05-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_format_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.IntegerField(choices=[(0, 'Учебный план'), (1, 'Рабочая программа')], default=0, verbose_name='Тип программы'),
        ),
    ]