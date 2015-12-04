# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hummingbird', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdevice',
            name='user_id',
        ),
        migrations.AddField(
            model_name='userdevice',
            name='user_profile',
            field=models.ForeignKey(to='hummingbird.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
    ]
