# Generated by Django 3.1.5 on 2021-01-31 08:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0005_auto_20210131_0330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='closetimages',
            old_name='thumnail',
            new_name='thumbnail',
        ),
        migrations.AlterField(
            model_name='closetpost',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
