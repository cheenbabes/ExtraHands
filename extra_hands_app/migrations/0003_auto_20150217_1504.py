# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0002_available_time_email_list_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='teacher',
            field=models.ForeignKey(to='extra_hands_app.Teacher', blank=True),
        ),
    ]
