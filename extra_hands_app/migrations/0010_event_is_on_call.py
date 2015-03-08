# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0009_event_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_on_call',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
