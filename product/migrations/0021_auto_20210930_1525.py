# Generated by Django 3.2.7 on 2021-09-30 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_alter_product_nutriscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='product.Category'),
        ),
        migrations.DeleteModel(
            name='Product_per_category',
        ),
    ]
