# Generated by Django 4.0.2 on 2022-02-15 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('currency_code', models.CharField(max_length=8)),
                ('alpha_code', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('type', models.CharField(choices=[('PURCHASE', 'Purchase'), ('SALE', 'Sale')], max_length=12)),
                ('net', models.DecimalField(decimal_places=2, max_digits=16)),
                ('vat', models.DecimalField(decimal_places=2, max_digits=16)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_country', to='fileproc.country')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_currency', to='fileproc.country')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRateHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('begin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_from', to='fileproc.country')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_to', to='fileproc.country')),
            ],
        ),
    ]
