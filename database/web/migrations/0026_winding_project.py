# Generated by Django 4.2.11 on 2024-05-30 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0025_alter_fiber_distributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='winding',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='web.project', verbose_name='Project Name'),
            preserve_default=False,
        ),
    ]