# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_hosting', '0003_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='url_image_name',
        ),
    ]
