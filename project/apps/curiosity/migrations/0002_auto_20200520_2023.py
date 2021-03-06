# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-20 20:23
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='curiosity.Post', verbose_name='Пост'),
        ),
        migrations.AddField(
            model_name='post',
            name='fimg',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=''), upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3a946096-fe9f-46b8-865c-dee49ea283c4'), primary_key=True, serialize=False, verbose_name='Интификатор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='curiosity_post_related', related_query_name='curiosity_posts', to='curiosity.Image', verbose_name='Первое изображение'),
        ),
    ]
