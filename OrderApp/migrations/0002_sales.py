# Generated by Django 5.0.6 on 2025-02-15 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
