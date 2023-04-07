# Generated by Django 4.1.7 on 2023-03-23 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='productvarient',
            name='varprice',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
