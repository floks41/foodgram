# Generated by Django 3.2.19 on 2023-07-06 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_ingredient_unique_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
    ]