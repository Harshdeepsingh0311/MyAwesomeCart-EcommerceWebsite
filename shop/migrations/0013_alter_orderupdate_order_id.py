# Generated by Django 3.2.3 on 2021-06-08 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20210608_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='order_id',
            field=models.IntegerField(default=0),
        ),
    ]