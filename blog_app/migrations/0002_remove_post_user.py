# Generated by Django 5.1.6 on 2025-02-26 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="user",
        ),
    ]
