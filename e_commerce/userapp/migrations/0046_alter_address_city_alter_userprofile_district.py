# Generated by Django 4.1.7 on 2023-03-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0045_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Ernakulam', 'Ernakulam'), ('Hubli', 'Hubli'), ('Coimbator', 'Coimbator'), ('Hydrabad', 'Hydrabad'), ('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Ernakulam', 'Ernakulam'), ('Hubli', 'Hubli'), ('Coimbator', 'Coimbator'), ('Hydrabad', 'Hydrabad'), ('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode')], max_length=20, null=True),
        ),
    ]
