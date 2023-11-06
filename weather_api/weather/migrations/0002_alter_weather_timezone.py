# Generated by Django 4.2.7 on 2023-11-03 13:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='timezone',
            field=models.CharField(default=django.utils.timezone.get_current_timezone, max_length=63),
        ),
    ]