# Generated by Django 5.0.1 on 2024-04-04 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_customer_email_alter_manufacturer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='product_images/%Y/%m/%d/'),
        ),
    ]
