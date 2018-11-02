# Generated by Django 2.1.2 on 2018-11-02 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('forfilter', models.CharField(default='', max_length=255)),
                ('KeepForwardedCaption', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Channel',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.CharField(max_length=255)),
                ('output', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(max_length=255)),
                ('name', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'Filter',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('number', models.CharField(max_length=15)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('self_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Session',
            },
        ),
        migrations.CreateModel(
            name='TeleBot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='filters',
            field=models.ManyToManyField(to='admin_panel.Filter'),
        ),
    ]
