# Generated by Django 3.2.7 on 2021-12-11 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211210_0638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pin_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='society_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='society_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='society_registration_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state',
        ),
    ]
