# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 05:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_id', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
    ]