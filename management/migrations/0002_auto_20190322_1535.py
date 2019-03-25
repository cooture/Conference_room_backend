# Generated by Django 2.1.7 on 2019-03-22 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting_user_rel',
            options={'verbose_name': '会议对象', 'verbose_name_plural': '会议对象'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(max_length=50),
        ),
    ]