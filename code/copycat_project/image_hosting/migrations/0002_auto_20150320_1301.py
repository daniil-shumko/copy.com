# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_hosting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
