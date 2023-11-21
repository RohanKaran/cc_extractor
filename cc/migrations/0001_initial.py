# Generated by Django 4.2.7 on 2023-11-21 10:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "videoId",
                    models.CharField(max_length=64, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("upload_date", models.DateTimeField(default=datetime.datetime.utcnow)),
                ("url", models.CharField(max_length=200)),
            ],
        ),
    ]
