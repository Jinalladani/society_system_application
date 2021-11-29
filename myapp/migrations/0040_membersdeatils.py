# Generated by Django 3.2.7 on 2021-11-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_auto_20211123_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembersDeatils',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flatNo', models.CharField(max_length=200)),
                ('primaryName', models.CharField(blank=True, max_length=200, null=True)),
                ('primaryContactNo', models.CharField(blank=True, max_length=10, null=True)),
                ('secondaryName', models.CharField(blank=True, max_length=200, null=True)),
                ('secondaryContactNo', models.CharField(blank=True, max_length=10, null=True)),
                ('accountingName', models.CharField(blank=True, max_length=200, null=True)),
                ('whatsappContactNo', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]