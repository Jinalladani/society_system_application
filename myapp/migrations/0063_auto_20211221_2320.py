# Generated by Django 3.2.7 on 2021-12-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0062_alter_balancevalue_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income_expense_ledgervalue1',
            name='closing_balance_bank',
            field=models.FloatField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='income_expense_ledgervalue1',
            name='closing_balance_cash',
            field=models.FloatField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='income_expense_ledgervalue1',
            name='opening_balance_bank',
            field=models.FloatField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='income_expense_ledgervalue1',
            name='opening_balance_cash',
            field=models.FloatField(blank=True, max_length=100, null=True),
        ),
    ]
