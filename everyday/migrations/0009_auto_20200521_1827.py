# Generated by Django 3.0.4 on 2020-05-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everyday', '0008_auto_20200520_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='newevent',
            name='kw1',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='newevent',
            name='kw2',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='newevent',
            name='kw3',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
