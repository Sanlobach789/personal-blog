# Generated by Django 3.2 on 2021-05-02 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalpage',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
