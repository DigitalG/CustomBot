# Generated by Django 2.1.2 on 2018-11-02 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_adminchannel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminchannel',
            name='KeepForwardedCaption',
        ),
        migrations.RemoveField(
            model_name='adminchannel',
            name='filters',
        ),
    ]
