# Generated by Django 4.1.7 on 2023-03-19 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0004_cartitem_provar_wishlist_provar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=50),
        ),
    ]
