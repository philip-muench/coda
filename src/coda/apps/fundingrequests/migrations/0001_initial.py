# Generated by Django 4.2.8 on 2024-04-26 14:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("publications", "0001_initial"),
        ("authors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExternalFunding",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("project_id", models.CharField()),
                ("project_name", models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name="FundingOrganization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "hexcolor",
                    models.CharField(
                        max_length=7,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Color must be in the format #RRGGBB",
                                regex="^#[a-fA-F0-9]{6}$",
                            )
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FundingRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("request_id", models.CharField(max_length=25, unique=True)),
                ("estimated_cost", models.DecimalField(decimal_places=2, max_digits=10)),
                ("estimated_cost_currency", models.CharField(max_length=3)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("direct", "Direct"),
                            ("reimbursement", "Reimbursement"),
                            ("unknown", "Unknown"),
                        ],
                        default="unknown",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "processing_status",
                    models.CharField(
                        choices=[
                            ("approved", "Approved"),
                            ("in_progress", "In Progress"),
                            ("rejected", "Rejected"),
                        ],
                        default="in_progress",
                        max_length=20,
                    ),
                ),
                (
                    "external_funding",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="fundingrequests.externalfunding",
                    ),
                ),
                (
                    "labels",
                    models.ManyToManyField(related_name="requests", to="fundingrequests.label"),
                ),
                (
                    "publication",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="publications.publication"
                    ),
                ),
                (
                    "submitter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="funding_requests",
                        to="authors.author",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="externalfunding",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="fundingrequests.fundingorganization",
            ),
        ),
    ]
