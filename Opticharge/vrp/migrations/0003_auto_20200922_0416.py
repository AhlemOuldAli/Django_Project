# Generated by Django 2.1.15 on 2020-09-22 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vrp', '0002_auto_20200910_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planification',
            name='generationnumber',
        ),
        migrations.RemoveField(
            model_name='planification',
            name='sizepopulation',
        ),
    ]