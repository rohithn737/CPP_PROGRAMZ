# Generated by Django 4.2.6 on 2023-10-31 17:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0006_thought_profile_pic"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="thought",
            name="profile_pic",
        ),
    ]