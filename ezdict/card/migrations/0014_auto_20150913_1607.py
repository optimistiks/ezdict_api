# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0013_auto_20150913_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardmeaning',
            name='card',
            field=models.ForeignKey(related_name='meanings', to='card.Card'),
        ),
        migrations.AlterField(
            model_name='cardmeaning',
            name='user',
            field=models.ForeignKey(related_name='meanings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cardtostudy',
            name='card',
            field=models.OneToOneField(related_name='to_study', to='card.Card'),
        ),
        migrations.AlterField(
            model_name='cardtostudy',
            name='user',
            field=models.ForeignKey(related_name='to_studies', to=settings.AUTH_USER_MODEL),
        ),
    ]
