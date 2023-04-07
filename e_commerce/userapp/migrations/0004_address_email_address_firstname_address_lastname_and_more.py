# Generated by Django 4.1.7 on 2023-03-06 15:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_alter_userprofile_district_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='email',
            field=models.EmailField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='firstname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='lastname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Mobile number should only contain digits', regex='^\\d+$')]),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Ernakulam', 'Ernakulam')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Ernakulam', 'Ernakulam')], max_length=20, null=True),
        ),
    ]
