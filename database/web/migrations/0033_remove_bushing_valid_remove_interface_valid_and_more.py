# Generated by Django 4.2.11 on 2024-06-03 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_alter_bushing_valid_alter_fiber_valid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bushing',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='interface',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='link',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='winding',
            name='valid',
        ),
    ]