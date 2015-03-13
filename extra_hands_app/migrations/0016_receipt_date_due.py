# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0015_account_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='date_due',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 20, 38, 52, 426000)),
            preserve_default=True,
        ),
    ]
