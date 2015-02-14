# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('whosgoing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inviteId', models.CharField(default=uuid.uuid4, max_length=36)),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('address', models.EmailField(max_length=254)),
                ('event', models.ForeignKey(to='whosgoing.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
