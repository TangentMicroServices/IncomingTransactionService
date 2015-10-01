# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomingrequest',
            name='created',
            field=models.DateTimeField(db_index=True, auto_now_add=True, default=datetime.datetime(2015, 9, 23, 9, 43, 59, 323902, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='incomingrequest',
            name='last_edited',
            field=models.DateTimeField(db_index=True, auto_now=True, default=datetime.datetime(2015, 9, 23, 9, 44, 9, 19584, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
