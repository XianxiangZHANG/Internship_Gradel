# Generated by Django 4.2.11 on 2024-06-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0033_remove_bushing_valid_remove_interface_valid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winding',
            name='link',
            field=models.CharField(max_length=255, verbose_name='Link Name'),
        ),
    ]
