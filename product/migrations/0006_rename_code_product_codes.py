# Generated by Django 3.2.7 on 2021-09-23 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20210923_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='code',
            new_name='codes',
        ),
    ]
