# Generated by Django 3.2.7 on 2021-10-05 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_alter_income_expense_ledger_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='account',
            field=models.FloatField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='balance_amount',
            field=models.FloatField(max_length=500),
        ),
        migrations.AlterField(
            model_name='income_expense_ledger',
            name='closing_balance_bank',
            field=models.FloatField(max_length=100),
        ),
        migrations.AlterField(
            model_name='income_expense_ledger',
            name='closing_balance_cash',
            field=models.FloatField(max_length=100),
        ),
        migrations.AlterField(
            model_name='income_expense_ledger',
            name='opening_balance_bank',
            field=models.FloatField(max_length=100),
        ),
        migrations.AlterField(
            model_name='income_expense_ledger',
            name='opening_balance_cash',
            field=models.FloatField(max_length=100),
        ),
    ]
