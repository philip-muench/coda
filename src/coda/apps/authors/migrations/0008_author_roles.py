# Generated by Django 4.2.8 on 2024-03-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authors", "0007_rename_person_personid"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="roles",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]