# Generated by Django 4.2.8 on 2024-02-27 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("publications", "0005_rename_publications_link_publication"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="publication",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="links",
                to="publications.publication",
            ),
        ),
    ]
