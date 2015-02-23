# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whosgoing', '0009_data__attendance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occurrencemember',
            old_name='attendence',
            new_name='attendance',
        ),
    ]
