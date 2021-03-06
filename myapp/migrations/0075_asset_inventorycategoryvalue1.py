# Generated by Django 3.2.7 on 2021-12-28 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0074_delete_membersdeatils'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset_InventoryCategoryValue1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(blank=True, max_length=200, null=True)),
                ('assetCategory', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.FloatField(blank=True, max_length=200, null=True)),
                ('purchasePrice', models.FloatField(blank=True, max_length=200, null=True)),
                ('deprecatedPrice', models.FloatField(blank=True, max_length=200, null=True)),
                ('onDate', models.DateField(blank=True, null=True)),
                ('totalCost', models.FloatField(blank=True, max_length=200, null=True)),
                ('marketValue', models.FloatField(blank=True, max_length=200, null=True)),
                ('society_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.society')),
            ],
        ),
    ]
