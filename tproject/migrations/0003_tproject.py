# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tproject', '0002_tproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='key',
            field=models.CharField(default='TFLOW', max_length=255),
            preserve_default=False,
        ),
    ]
