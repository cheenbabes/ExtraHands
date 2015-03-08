# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0005_auto_20150220_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='clicks',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
