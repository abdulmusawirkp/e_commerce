# Generated by Django 4.1.7 on 2023-03-08 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0011_alter_address_city_alter_userprofile_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Kannur', 'Kannur'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Coimbator', 'Coimbator')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Kannur', 'Kannur'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Coimbator', 'Coimbator')], max_length=20, null=True),
        ),
    ]
