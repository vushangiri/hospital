# Generated by Django 3.0.8 on 2020-09-28 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_auto_20200928_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
