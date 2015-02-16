# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.CharField(max_length=128)),
                ('street', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=2)),
                ('phone_number', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=600)),
                ('client_slug', models.SlugField(unique=True)),
                ('campus', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=2)),
                ('phone_number', models.CharField(max_length=15)),
                ('ect_qualified', models.BooleanField(default=False)),
                ('cpr_first_aid', models.BooleanField(default=False)),
                ('universal_precautions', models.BooleanField(default=False)),
                ('qualifications', models.CharField(max_length=300)),
                ('degree', models.CharField(max_length=30)),
                ('major', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=False)),
                ('on_call', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
