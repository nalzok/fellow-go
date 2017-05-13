# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pickup', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fellow',
            options={'verbose_name': 'fellow', 'verbose_name_plural': 'fellows'},
        ),
        migrations.AlterField(
            model_name='fellow',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active?'),
        ),
        migrations.AlterField(
            model_name='fellow',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='is admin?'),
        ),
    ]