# Generated by Django 3.2.7 on 2021-12-30 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0077_auto_20211229_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='subuser1',
            name='user_key',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
