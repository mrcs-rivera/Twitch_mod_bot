# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bot_commands', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='standard_commands',
            fields=[
                ('command', models.CharField(max_length=200, unique=True, serialize=False, primary_key=True)),
                ('command_type', models.CharField(max_length=512)),
                ('message', models.CharField(max_length=512)),
                ('userlevel', models.CharField(max_length=15, choices=[(b'm', b'mod'), (b's', b'subscriber'), (b'e', b'everyone')])),
            ],
        ),
        migrations.AddField(
            model_name='custom_commands',
            name='command_type',
            field=models.CharField(default=datetime.datetime(2016, 8, 1, 22, 7, 46, 744409, tzinfo=utc), max_length=512),
            preserve_default=False,
        ),
    ]
