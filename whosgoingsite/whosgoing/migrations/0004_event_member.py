# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whosgoing', '0003_rename_emailInvitiation'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('event', models.ForeignKey(to='whosgoing.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventmember',
            unique_together=set([('user', 'event')]),
        ),
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(related_name='events', through='whosgoing.EventMember', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
