# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0003_auto_20150826_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='article',
            field=models.TextField(default=b'NULL', null=True),
        ),
    ]
