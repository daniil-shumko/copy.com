# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to=b'images/')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('views', models.IntegerField(default=0)),
                ('up_votes', models.IntegerField(default=0)),
                ('down_votes', models.IntegerField(default=0)),
                ('category', models.ForeignKey(to='image_hosting.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
