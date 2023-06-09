# Generated by Django 4.1.7 on 2023-03-08 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0016_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Madurai', 'Madurai'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Banglore', 'Banglore')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Madurai', 'Madurai'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Banglore', 'Banglore')], max_length=20, null=True),
        ),
    ]
