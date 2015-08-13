# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0003_auto_20150812_1842'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wordtolearn',
            unique_together=set([('user', 'string')]),
        ),
    ]
