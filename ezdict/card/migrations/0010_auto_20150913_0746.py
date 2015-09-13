# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0009_auto_20150911_0600'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardToStudy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(related_name='card_to_study', to='card.Card')),
                ('user', models.ForeignKey(related_name='card_to_study', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cardtostudy',
            unique_together=set([('user', 'card')]),
        ),
    ]
