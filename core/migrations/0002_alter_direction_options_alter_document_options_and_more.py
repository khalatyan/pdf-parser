# Generated by Django 4.0.4 on 2022-05-09 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='direction',
            options={'verbose_name': 'направление', 'verbose_name_plural': 'Направления'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'документ', 'verbose_name_plural': 'Документы'},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name': 'факультет', 'verbose_name_plural': 'Факультеты'},
        ),
        migrations.AlterModelOptions(
            name='format',
            options={'verbose_name': 'формат', 'verbose_name_plural': 'Форматы обучения'},
        ),
        migrations.AlterField(
            model_name='document',
            name='format',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.format', verbose_name='Формат обучения'),
        ),
        migrations.AlterField(
            model_name='format',
            name='direction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.direction', verbose_name='Направление'),
        ),
    ]
