# Generated by Django 4.2.6 on 2024-06-09 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_procedure_client_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='data_path',
            field=models.CharField(max_length=255),
        ),
    ]
