# Generated by Django 4.1.7 on 2023-03-24 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0050_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Kannur', 'Kannur'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Kannur', 'Kannur'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=20, null=True),
        ),
    ]
