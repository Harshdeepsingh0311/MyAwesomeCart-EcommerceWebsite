# Generated by Django 3.2.3 on 2021-06-09 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='chead0',
            field=models.CharField(default='HEllo WOrld', max_length=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='chead1',
            field=models.CharField(default='HEllo WOrld', max_length=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='chead2',
            field=models.CharField(default='HEllo WOrld', max_length=5000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='head0',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='head1',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='head2',
            field=models.CharField(max_length=500),
        ),
    ]