# Generated by Django 4.2.8 on 2024-06-12 12:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("publications", "0007_remove_publication_print_publication_state"),
    ]

    operations = [
        migrations.RenameField(
            model_name="publication",
            old_name="online_publication_state",
            new_name="publication_state",
        ),
    ]