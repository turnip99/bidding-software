# Generated by Django 4.0.5 on 2022-06-07 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0015_alter_auctiondescriptionbulletpoint_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionsetting',
            name='payment_reference',
            field=models.CharField(blank=True, default='*your name*', help_text='Used in the message generator.', max_length=20, null=True),
        ),
    ]
