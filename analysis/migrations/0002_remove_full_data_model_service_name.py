# Generated by Django 4.0.4 on 2022-05-18 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='full_data_model',
            name='service_name',
        ),
    ]
