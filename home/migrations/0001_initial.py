# Generated by Django 3.1 on 2020-09-08 06:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('desc', models.TextField()),
                ('report_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='indexing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='search_text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_text', models.CharField(max_length=255)),
                ('visit_couont', models.IntegerField(default=0)),
                ('priority', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='sites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=400)),
                ('domain', models.CharField(default='.com', max_length=20)),
                ('display', models.BooleanField(default=True)),
                ('visit_count', models.IntegerField(default=0)),
                ('priority', models.FloatField(default=1.0)),
                ('indexed', models.BooleanField(default=False)),
                ('words_links', models.CharField(default='-', max_length=255)),
                ('icon', models.CharField(default='/favicon.ico', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='uncrawled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
            ],
        ),
    ]
