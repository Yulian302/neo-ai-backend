# Generated by Django 4.2.9 on 2024-01-09 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0006_rename_notifications_usernotification_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="usernotification",
            name="success_number",
            field=models.IntegerField(default=1),
        ),
    ]