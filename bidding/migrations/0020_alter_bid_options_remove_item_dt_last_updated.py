# Generated by Django 4.0.5 on 2022-06-17 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0019_auctionsetting_bid_sync_regularity_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ('-price',)},
        ),
        migrations.RemoveField(
            model_name='item',
            name='dt_last_updated',
        ),
    ]
