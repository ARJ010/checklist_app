# Generated by Django 4.2.6 on 2024-06-23 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0003_remove_procedureresponse_return_resone'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedureresponse',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='procedureresponse',
            name='user_response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
