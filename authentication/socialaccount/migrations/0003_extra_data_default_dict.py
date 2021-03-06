# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import authentication.socialaccount.fields


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0002_token_max_lengths'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialaccount',
            name='extra_data',
            field=authentication.socialaccount.fields.JSONField(default=dict, verbose_name='extra data'),
            preserve_default=True,
        ),
    ]
