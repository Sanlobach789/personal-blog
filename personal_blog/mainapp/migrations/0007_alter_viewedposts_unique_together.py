# Generated by Django 3.2 on 2021-05-02 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20210502_1547'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='viewedposts',
            unique_together=set(),
        ),
    ]