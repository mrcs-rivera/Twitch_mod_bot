# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_commands', '0002_auto_20160801_2207'),
    ]

    operations = [
        migrations.DeleteModel(
            name='standard_commands',
        ),
    ]
