# Generated by Django 5.1.4 on 2025-01-18 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_shopifyorder_updated_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopifyorder',
            old_name='customer_name',
            new_name='customer',
        ),
    ]
