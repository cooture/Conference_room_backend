# Generated by Django 2.1.7 on 2019-03-26 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_auto_20190326_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.ImageField(default='null', upload_to='static/facelib'),
        ),
    ]