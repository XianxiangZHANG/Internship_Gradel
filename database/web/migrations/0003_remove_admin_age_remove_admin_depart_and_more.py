# Generated by Django 4.2.11 on 2024-05-07 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_admin_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='age',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='depart',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='gender',
        ),
    ]
