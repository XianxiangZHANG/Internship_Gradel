# Generated by Django 4.2.11 on 2024-05-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_alter_resin_hardener_alter_resin_manufacturer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Last Update M/D/Y'),
        ),
    ]