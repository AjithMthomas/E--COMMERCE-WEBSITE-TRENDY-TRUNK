# Generated by Django 4.1.5 on 2023-01-19 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.IntegerField(max_length=50),
        ),
    ]
