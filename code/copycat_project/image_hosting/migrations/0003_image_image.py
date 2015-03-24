# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_hosting', '0002_auto_20150320_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default='', upload_to=b'images/'),
            preserve_default=False,
        ),
    ]
