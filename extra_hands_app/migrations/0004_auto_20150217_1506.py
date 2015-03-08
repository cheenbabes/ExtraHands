# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0003_auto_20150217_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='teacher',
            field=models.ForeignKey(default=None, blank=True, to='extra_hands_app.Teacher', null=True),
        ),
    ]
