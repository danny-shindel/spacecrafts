# Generated by Django 3.1.7 on 2021-04-16 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210416_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='craft',
        ),
        migrations.AddField(
            model_name='craft',
            name='badges',
            field=models.ManyToManyField(to='main_app.Badge'),
        ),
    ]