# Generated by Django 3.2.3 on 2021-06-09 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210609_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnail',
            field=models.ImageField(upload_to='blog/images'),
        ),
    ]