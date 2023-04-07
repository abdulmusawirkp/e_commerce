# Generated by Django 4.1.7 on 2023-03-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0023_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Kozhikkode', 'Kozhikkode'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Ernakulam', 'Ernakulam'), ('Banglore', 'Banglore'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Kozhikkode', 'Kozhikkode'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Ernakulam', 'Ernakulam'), ('Banglore', 'Banglore'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli')], max_length=20, null=True),
        ),
    ]
