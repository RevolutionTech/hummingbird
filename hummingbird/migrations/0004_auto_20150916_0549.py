# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hummingbird', '0003_auto_20150915_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_played',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
