# Generated by Django 3.2.11 on 2022-03-09 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gd', '0008_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='time',
            field=models.CharField(max_length=50),
        ),
    ]
