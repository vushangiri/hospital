# Generated by Django 3.0.8 on 2020-09-28 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20200928_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
