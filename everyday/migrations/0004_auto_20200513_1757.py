# Generated by Django 3.0.4 on 2020-05-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everyday', '0003_auto_20200513_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newevent',
            name='end',
            field=models.DateField(null=True, verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='newevent',
            name='when',
            field=models.DateField(auto_now_add=True, verbose_name='When'),
        ),
    ]
