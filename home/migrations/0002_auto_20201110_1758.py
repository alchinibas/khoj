# Generated by Django 3.1.3 on 2020-11-10 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexing',
            name='site_ids',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='indexing',
            name='site_id',
            field=models.TextField(default=''),
        ),
    ]