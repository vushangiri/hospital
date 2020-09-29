# Generated by Django 3.0.8 on 2020-09-28 07:31

import autoslug.fields
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='city',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='expertise',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='postalcode',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='first_name', unique=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='state',
            field=models.CharField(blank=True, choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='status',
            field=models.CharField(blank=True, choices=[('inactive', 'Inactive'), ('active', 'Active')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]