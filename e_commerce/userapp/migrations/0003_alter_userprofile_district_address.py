# Generated by Django 4.1.7 on 2023-03-06 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userapp', '0002_userprofile_address_userprofile_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Kannur', 'Kannur')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(choices=[('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Kannur', 'Kannur')], max_length=255)),
                ('state', models.CharField(choices=[('Kerala', 'Kerala'), ('Tamilnadu', 'Tamilnadu'), ('Karnataka', 'Karnataka'), ('AndraPradesh', 'AndraPradesh')], max_length=255)),
                ('pincode', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
