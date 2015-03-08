# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0012_auto_20150227_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='available_time',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
