# Generated by Django 3.0.6 on 2020-06-28 05:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20200628_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='report_date',
            field=models.DateField(default=datetime.datetime(2020, 6, 28, 5, 13, 52, 169230, tzinfo=utc)),
        ),
    ]
