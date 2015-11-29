# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hummingbird', '0005_auto_20150923_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_id',
        ),
    ]
