# Generated by Django 3.1.6 on 2021-02-09 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20210209_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
