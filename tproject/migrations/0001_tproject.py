# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('url', models.CharField(max_length=255, null=True)),
                ('lead', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('url', models.CharField(max_length=255, null=True)),
                ('lead', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('team_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequirementType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]
