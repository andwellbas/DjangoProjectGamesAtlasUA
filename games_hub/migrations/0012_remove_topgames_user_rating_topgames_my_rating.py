# Generated by Django 4.2 on 2023-05-05 09:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_hub', '0011_remove_topgames_my_rating_topgames_user_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topgames',
            name='user_rating',
        ),
        migrations.AddField(
            model_name='topgames',
            name='my_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
