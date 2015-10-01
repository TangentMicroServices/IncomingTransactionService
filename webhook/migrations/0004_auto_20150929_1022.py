# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0003_incomingrequest_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingrequest',
            name='source',
            field=models.CharField(choices=[('IT', 'If This Then That'), ('HC', 'Hipchat'), ('UK', 'Unknown')], default='UK', max_length=2),
        ),
    ]
