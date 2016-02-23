# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0004_auto_20150929_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingrequest',
            name='source',
            field=models.CharField(max_length=10, choices=[('IT', 'If This Then That'), ('HC', 'Hipchat'), ('UK', 'Unknown')], default='UK'),
        ),
        migrations.AlterField(
            model_name='incomingrequest',
            name='user',
            field=models.IntegerField(default='-1'),
        ),
    ]
