# Generated by Django 3.0.6 on 2020-06-28 05:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20200628_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='report_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
