# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tproject', '0001_tproject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lead',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
