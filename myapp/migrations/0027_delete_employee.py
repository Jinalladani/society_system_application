# Generated by Django 3.2.7 on 2021-10-19 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_delete_income_expense_ledger'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
