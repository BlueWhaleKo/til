# Generated by Django 3.0.4 on 2020-03-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200308_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ohlc',
            name='change',
            field=models.FloatField(null=True),
        ),
    ]
