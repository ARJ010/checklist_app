# Generated by Django 4.2.6 on 2024-10-06 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0006_alter_procedureresponse_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedureresponse',
            name='response',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A'), ('-----', '-----')], max_length=10),
        ),
    ]
