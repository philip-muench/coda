# Generated by Django 4.2.8 on 2024-04-05 11:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fundingrequests", "0011_fundingrequest_external_funding"),
    ]

    operations = [
        migrations.AddField(
            model_name="fundingrequest",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("direct", "Direct"),
                    ("reimbursement", "Reimbursement"),
                    ("unknown", "Unknown"),
                ],
                default="unknown",
            ),
        ),
    ]
