# Generated by Django 2.2.16 on 2020-10-28 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0004_auto_20201028_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='sku',
            field=models.IntegerField(),
        ),
    ]
