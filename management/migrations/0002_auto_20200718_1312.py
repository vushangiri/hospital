# Generated by Django 3.0.8 on 2020-07-18 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='photo',
            field=models.ImageField(default=1, upload_to='pics'),
            preserve_default=False,
        ),
    ]
