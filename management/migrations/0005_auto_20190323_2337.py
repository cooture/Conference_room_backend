# Generated by Django 2.1.7 on 2019-03-23 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_auto_20190322_1547'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='meeting_user_rel',
            unique_together={('user', 'meeting')},
        ),
    ]