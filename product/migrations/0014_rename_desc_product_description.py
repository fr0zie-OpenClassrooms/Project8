# Generated by Django 3.2.7 on 2021-09-23 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='desc',
            new_name='description',
        ),
    ]
