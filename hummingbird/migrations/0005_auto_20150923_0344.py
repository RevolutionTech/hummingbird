# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hummingbird', '0004_auto_20150916_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='length',
            field=models.IntegerField(default=10, validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='song',
            field=models.FileField(null=True, upload_to=b'media/songs', blank=True),
        ),
    ]
