# Generated by Django 3.2.4 on 2021-06-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='base_price',
            field=models.FloatField(max_length=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='winning_price',
            field=models.FloatField(max_length=0),
        ),
    ]
