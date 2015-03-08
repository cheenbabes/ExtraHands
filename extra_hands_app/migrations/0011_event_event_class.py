# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0010_event_is_on_call'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_class',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
