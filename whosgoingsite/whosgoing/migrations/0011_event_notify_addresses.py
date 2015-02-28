# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '__first__'),
        ('whosgoing', '0010_rename_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notify_addresses',
            field=models.ManyToManyField(to='account.EmailAddress'),
            preserve_default=True,
        ),
    ]
