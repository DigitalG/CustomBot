# Generated by Django 2.1.2 on 2018-10-24 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0005_session_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='number',
            field=models.CharField(max_length=15),
        ),
    ]
