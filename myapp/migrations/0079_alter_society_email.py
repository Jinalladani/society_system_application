# Generated by Django 3.2.7 on 2021-12-30 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0078_subuser1_user_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
