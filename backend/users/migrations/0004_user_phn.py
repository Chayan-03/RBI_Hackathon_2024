# Generated by Django 5.0.7 on 2024-07-15 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_upi_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phn',
            field=models.IntegerField(default=1234),
        ),
    ]