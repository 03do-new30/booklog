# Generated by Django 3.1.6 on 2021-02-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0011_auto_20210216_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybook',
            name='score',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
