# Generated by Django 5.1.4 on 2024-12-26 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_products_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='vendor',
            field=models.CharField(default='', max_length=255),
        ),
    ]