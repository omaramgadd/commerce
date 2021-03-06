# Generated by Django 3.1.4 on 2020-12-25 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(default=' ', max_length=64),
        ),
        migrations.AddField(
            model_name='listing',
            name='url',
            field=models.CharField(default=' ', max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.IntegerField(default=' '),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(default=' ', max_length=64),
        ),
    ]
