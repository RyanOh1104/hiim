# Generated by Django 3.0.4 on 2020-05-20 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everyday', '0007_newevent_emoji'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newevent',
            name='when',
            field=models.DateField(verbose_name='When'),
        ),
    ]
