# Generated by Django 3.2.7 on 2021-12-09 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0049_rename_state1_user_society_deatils_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]
