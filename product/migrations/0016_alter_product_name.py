# Generated by Django 3.2.7 on 2021-09-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20210923_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]