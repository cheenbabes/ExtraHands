# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0008_auto_20150221_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='comments',
            field=models.CharField(default=b'', max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
