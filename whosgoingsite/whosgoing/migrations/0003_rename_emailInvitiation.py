# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('whosgoing', '0002_emailinvitation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmailInvitation',
            new_name='Invitation'
        ),
    ]
