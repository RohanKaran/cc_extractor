from datetime import datetime

from django.db.models import Model, TextField, CharField, DateTimeField
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model as PynamoModel


class ClosedCaption(PynamoModel):
    class Meta:
        table_name = "EcoWiser"
        region = "ap-south-1"

    videoId = UnicodeAttribute(hash_key=True)
    caption = UnicodeAttribute()
    startTime = UnicodeAttribute(range_key=True)
    endTime = UnicodeAttribute()
    url = UnicodeAttribute()


class Video(Model):
    videoId = CharField(primary_key=True, max_length=64)
    title = CharField(max_length=200)
    description = TextField()
    upload_date = DateTimeField(default=datetime.utcnow, db_index=True)
    url = CharField(max_length=200)
