# Generated by Django 4.2.6 on 2024-06-23 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0004_procedureresponse_remark_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='procedureresponse',
            old_name='remark',
            new_name='remarks',
        ),
    ]
