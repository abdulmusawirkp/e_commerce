# Generated by Django 4.1.7 on 2023-03-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0035_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Hydrabad', 'Hydrabad'), ('Ernakulam', 'Ernakulam'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Banglore', 'Banglore'), ('Coimbator', 'Coimbator'), ('Madurai', 'Madurai'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hydrabad', 'Hydrabad'), ('Ernakulam', 'Ernakulam'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Banglore', 'Banglore'), ('Coimbator', 'Coimbator'), ('Madurai', 'Madurai'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=20, null=True),
        ),
    ]
