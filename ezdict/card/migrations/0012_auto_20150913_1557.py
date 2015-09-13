# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0011_auto_20150913_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='user',
            field=models.ForeignKey(related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cardtostudy',
            name='card',
            field=models.ForeignKey(related_name='card_to_study', to='card.Card', unique=True),
        ),
    ]
