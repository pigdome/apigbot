# Generated by Django 3.1.5 on 2021-01-30 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0004_closetimages_thumnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closetimages',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]