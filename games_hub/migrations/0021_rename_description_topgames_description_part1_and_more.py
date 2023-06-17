# Generated by Django 4.2 on 2023-05-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_hub', '0020_alter_comment_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topgames',
            old_name='description',
            new_name='description_part1',
        ),
        migrations.AddField(
            model_name='topgames',
            name='description_part2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='topgames',
            name='publisher',
            field=models.CharField(max_length=100, null=True),
        ),
    ]