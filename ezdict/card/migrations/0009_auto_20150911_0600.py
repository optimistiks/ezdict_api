# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_auto_20150902_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardmeaning',
            name='card',
            field=models.ForeignKey(related_name='card_meanings', to='card.Card'),
        ),
        migrations.AlterField(
            model_name='cardmeaning',
            name='user',
            field=models.ForeignKey(related_name='card_meanings', to=settings.AUTH_USER_MODEL),
        ),
    ]
