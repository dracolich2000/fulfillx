# Generated by Django 5.1.4 on 2025-01-18 23:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_name', models.CharField(blank=True, max_length=255, null=True)),
                ('shop_url', models.URLField(unique=True)),
                ('access_token', models.TextField()),
                ('shop_platform', models.CharField(default='Shopify', max_length=50)),
                ('linked_by', models.CharField(blank=True, max_length=255, null=True)),
                ('linked_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopifyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('customer', models.CharField(blank=True, max_length=255, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField()),
                ('payment_status', models.CharField(blank=True, max_length=255, null=True)),
                ('fulfillment_status', models.CharField(blank=True, max_length=255, null=True)),
                ('delivery_status', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopifyOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='user.shopifyorder')),
            ],
        ),
    ]
