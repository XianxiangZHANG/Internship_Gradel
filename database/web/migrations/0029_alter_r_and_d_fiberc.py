# Generated by Django 4.2.11 on 2024-06-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0028_alter_r_and_d_fiberc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='r_and_d',
            name='fiberC',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]