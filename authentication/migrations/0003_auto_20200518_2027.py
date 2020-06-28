# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-18 20:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_emailaddress_emailconfirmation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailaddress',
            name='user',
        ),
        migrations.RemoveField(
            model_name='emailconfirmation',
            name='email_address',
        ),
        migrations.DeleteModel(
            name='EmailAddress',
        ),
        migrations.DeleteModel(
            name='EmailConfirmation',
        ),
    ]
