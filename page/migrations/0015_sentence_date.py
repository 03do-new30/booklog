# Generated by Django 3.1.6 on 2021-02-16 16:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0014_sentence_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
