# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tproject', '0003_tproject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='key',
            new_name='project_key',
        ),
    ]
