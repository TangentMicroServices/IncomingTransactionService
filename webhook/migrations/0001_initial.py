# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingRequest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('source', models.CharField(blank=True, null=True, max_length=100)),
                ('incoming_url', models.URLField(blank=True, null=True)),
                ('payload', models.TextField(default='{}')),
            ],
        ),
    ]
