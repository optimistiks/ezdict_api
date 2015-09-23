# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0014_auto_20150913_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardIsLearned',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card', models.OneToOneField(related_name='is_learned', to='card.Card')),
                ('user', models.ForeignKey(related_name='learned_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cardislearned',
            unique_together=set([('user', 'card')]),
        ),
    ]
