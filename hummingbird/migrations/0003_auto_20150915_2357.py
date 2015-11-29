# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hummingbird', '0002_auto_20150915_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='song',
            field=models.FileField(null=True, upload_to=b'songs', blank=True),
        ),
    ]
