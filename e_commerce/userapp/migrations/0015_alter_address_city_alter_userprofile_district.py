# Generated by Django 4.1.7 on 2023-03-08 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0014_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Kozhikkode', 'Kozhikkode'), ('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Ernakulam', 'Ernakulam')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Kozhikkode', 'Kozhikkode'), ('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Ernakulam', 'Ernakulam')], max_length=20, null=True),
        ),
    ]
