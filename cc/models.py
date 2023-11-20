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
