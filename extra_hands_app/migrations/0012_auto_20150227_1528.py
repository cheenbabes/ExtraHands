# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0011_event_event_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='available_time',
            name='event_class',
            field=models.CharField(default=b'event-warning', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_class',
            field=models.CharField(default=b'event-info', max_length=100),
            preserve_default=True,
        ),
    ]
