# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0007_auto_20150830_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardMeaning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=255)),
                ('card', models.ForeignKey(related_name='card_meaning', to='card.Card')),
                ('user', models.ForeignKey(related_name='card_meaning', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cardmeaning',
            unique_together=set([('card', 'text')]),
        ),
    ]
