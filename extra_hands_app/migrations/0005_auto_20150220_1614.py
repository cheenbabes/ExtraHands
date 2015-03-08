# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0004_auto_20150217_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='campus',
            field=models.IntegerField(default=1),
        ),
    ]
