# Generated by Django 4.2.7 on 2023-11-21 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cc", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="upload_date",
            field=models.DateTimeField(db_index=True, default=datetime.datetime.utcnow),
        ),
    ]
