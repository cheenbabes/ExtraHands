# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra_hands_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Available_Time',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('teacher', models.ForeignKey(to='extra_hands_app.Teacher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Email_List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_open', models.BooleanField(default=False)),
                ('in_progress', models.BooleanField(default=False)),
                ('client', models.ForeignKey(to='extra_hands_app.Client')),
                ('teacher', models.ForeignKey(to='extra_hands_app.Teacher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
