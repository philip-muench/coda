# Generated by Django 4.2.8 on 2024-02-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fundingrequests", "0004_alter_fundingrequest_request_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fundingrequest",
            name="processing_status",
            field=models.CharField(
                choices=[
                    ("approved", "Approved"),
                    ("in_progress", "In Progress"),
                    ("rejected", "Rejected"),
                ],
                default="in_progress",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="fundingrequest",
            name="request_id",
            field=models.CharField(default="coda-88ea9519-2024-02-26", max_length=25, unique=True),
        ),
    ]
