# Generated by Django 3.2.7 on 2021-12-08 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0045_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_society_deatils',
            name='state',
            field=models.CharField(default='Gujarat', max_length=100),
        ),
    ]
