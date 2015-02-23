# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whosgoing', '0007_eventoccurrence'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OccurrenceMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('attendence', models.ForeignKey(to='whosgoing.Attendance', default=1)),
                ('occurrence', models.ForeignKey(to='whosgoing.EventOccurrence')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='occurrencemember',
            unique_together=set([('user', 'occurrence')]),
        ),
        migrations.AddField(
            model_name='eventoccurrence',
            name='members',
            field=models.ManyToManyField(through='whosgoing.OccurrenceMember', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
