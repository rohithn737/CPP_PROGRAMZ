# Generated by Django 4.2.6 on 2023-10-31 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0005_posting"),
    ]

    operations = [
        migrations.AddField(
            model_name="thought",
            name="profile_pic",
            field=models.ImageField(
                blank=True, default="Default1.png", null=True, upload_to=""
            ),
        ),
    ]
