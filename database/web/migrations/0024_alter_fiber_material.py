# Generated by Django 4.2.11 on 2024-05-30 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0023_sequencetype_alter_part_partname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiber',
            name='material',
            field=models.CharField(default=1, max_length=255, verbose_name='Material'),
            preserve_default=False,
        ),
    ]