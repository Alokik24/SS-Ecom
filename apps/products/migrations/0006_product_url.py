# Generated by Django 5.2.2 on 2025-06-13 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_product_in_stock_category_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(blank=True, default=''),
        ),
    ]
