# Generated by Django 4.2.11 on 2024-05-15 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_interface_part_interface_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interface',
            name='bushing',
        ),
    ]
