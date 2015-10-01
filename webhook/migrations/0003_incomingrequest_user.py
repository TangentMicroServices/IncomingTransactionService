# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0002_auto_20150923_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomingrequest',
            name='user',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
