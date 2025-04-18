# Generated by Django 5.0.6 on 2024-09-08 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_at', models.DateTimeField(auto_now=True)),
                ('table_number', models.IntegerField()),
                ('paycheck', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('rest', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=0)),
                ('provided', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderApp.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderApp.products')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='products',
            field=models.ManyToManyField(related_name='customers', to='OrderApp.products'),
        ),
    ]
