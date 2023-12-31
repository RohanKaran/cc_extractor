from django.db.models import CharField, DateTimeField, Model, TextField
from django.utils.timezone import now
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
    upload_date = DateTimeField(default=now, db_index=True)
    url = CharField(max_length=200)
