# Generated by Django 3.1.6 on 2021-02-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0008_auto_20210216_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='mybook',
            name='acc_id',
            field=models.CharField(default='default', max_length=20),
        ),
    ]
