# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_auto_20150826_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='article',
            field=models.TextField(null=True),
        ),
    ]
