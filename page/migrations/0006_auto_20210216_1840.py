# Generated by Django 3.1.6 on 2021-02-16 09:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_auto_20210216_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='mybook',
            name='end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mybook',
            name='start',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
