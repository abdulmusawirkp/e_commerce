# Generated by Django 4.1.7 on 2023-03-17 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0037_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Kannur', 'Kannur'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Banglore', 'Banglore'), ('Madurai', 'Madurai'), ('Kozhikkode', 'Kozhikkode'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Ernakulam', 'Ernakulam')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Kannur', 'Kannur'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Banglore', 'Banglore'), ('Madurai', 'Madurai'), ('Kozhikkode', 'Kozhikkode'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Ernakulam', 'Ernakulam')], max_length=20, null=True),
        ),
    ]
