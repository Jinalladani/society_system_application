# Generated by Django 3.2.7 on 2021-11-23 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_filestorevalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income_Expense_LedgerValue1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOn', models.DateField()),
                ('type', models.CharField(max_length=100)),
                ('amount', models.FloatField(max_length=100)),
                ('category_header', models.CharField(blank=True, max_length=100, null=True)),
                ('from_or_to_account', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_type', models.CharField(max_length=100)),
                ('transaction_details', models.CharField(blank=True, max_length=100, null=True)),
                ('voucherNo_or_invoiceNo', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='image')),
                ('remark', models.TextField(blank=True, max_length=500, null=True)),
                ('opening_balance_cash', models.FloatField(max_length=100)),
                ('closing_balance_cash', models.FloatField(max_length=100)),
                ('opening_balance_bank', models.FloatField(max_length=100)),
                ('closing_balance_bank', models.FloatField(max_length=100)),
                ('entry_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileStoreValue1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=100, null=True)),
                ('type_file', models.FileField(blank=True, null=True, upload_to='filestore/', verbose_name='file')),
                ('income_Expense_LedgerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.income_expense_ledgervalue1')),
            ],
        ),
    ]
