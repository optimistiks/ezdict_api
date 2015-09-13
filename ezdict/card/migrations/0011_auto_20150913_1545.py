# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0010_auto_20150913_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtostudy',
            name='card',
            field=models.ForeignKey(related_name='cards_to_study', to='card.Card'),
        ),
        migrations.AlterField(
            model_name='cardtostudy',
            name='user',
            field=models.ForeignKey(related_name='cards_to_study', to=settings.AUTH_USER_MODEL),
        ),
    ]
