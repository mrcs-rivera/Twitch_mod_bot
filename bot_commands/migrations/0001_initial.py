# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='custom_commands',
            fields=[
                ('command', models.CharField(max_length=200, unique=True, serialize=False, primary_key=True)),
                ('message', models.CharField(max_length=512)),
                ('userlevel', models.CharField(max_length=15, choices=[(b'm', b'mod'), (b's', b'subscriber'), (b'e', b'everyone')])),
            ],
        ),
    ]
