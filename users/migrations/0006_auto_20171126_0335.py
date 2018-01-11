# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-26 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20171126_0331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nearest_users',
        ),
        migrations.AddField(
            model_name='user',
            name='nearest_users',
            field=models.ManyToManyField(related_name='_user_nearest_users_+', to='users.User'),
        ),
    ]
