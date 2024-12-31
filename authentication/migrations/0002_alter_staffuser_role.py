# Generated by Django 5.1.4 on 2024-12-23 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('User', 'User'), ('Vendor', 'Vendor')], default='user', max_length=10),
        ),
    ]