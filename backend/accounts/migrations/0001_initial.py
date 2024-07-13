# Generated by Django 5.0.7 on 2024-07-13 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LockingSystemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.BooleanField(default=False)),
                ('debit', models.BooleanField(default=False)),
                ('net_banking', models.BooleanField(default=False)),
                ('upi', models.BooleanField(default=False)),
                ('banking_app', models.BooleanField(default=False)),
            ],
        ),
    ]
