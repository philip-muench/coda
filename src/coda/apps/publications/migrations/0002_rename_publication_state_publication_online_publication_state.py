# Generated by Django 4.2.8 on 2024-06-10 12:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("publications", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="publication",
            old_name="publication_state",
            new_name="online_publication_state",
        ),
    ]
