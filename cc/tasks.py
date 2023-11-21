import hashlib
import re
import subprocess

from celery import shared_task
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now

from cc.models import ClosedCaption, Video


@shared_task
def run_ccextractor(video_path, file_url):
    storage = FileSystemStorage()
    hash_md5 = hashlib.md5()
    with storage.open(video_path, "rb") as file:
        for chunk in iter(lambda: file.read(10485760), b""):
            hash_md5.update(chunk)
    video_file_hash = hash_md5.hexdigest()
    try:
        video = Video.objects.get(pk=video_file_hash)
        video.url = file_url
        video.upload_date = now()
        video.save()
    except Video.DoesNotExist:
        Video.objects.create(
            videoId=video_file_hash,
            title=video_path.split("/")[-1],
            description="",
            url=file_url,
        )
    cc = ClosedCaption.query(video_file_hash, limit=1)
    count = 0
    for _ in cc:
        count += 1
    if count > 0:
        print("cc found")
        storage.delete(video_path)
        return

    subtitle_path = storage.get_available_name("subtitles.srt")
    command = [
        r"ccextractor",
        video_path,
        "-o",
        subtitle_path,
    ]
    subprocess.run(command)
    subtitles = []
    with storage.open(subtitle_path, "r") as file:
        subtitle_text = file.read()
        pattern = (
            r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n\s*(.+?)\n\n"
        )
        matches = re.findall(pattern, subtitle_text, re.DOTALL)
        for m in matches:
            cleaned_text = " ".join([line.strip() for line in m[2].split("\n")])
            subtitles.append({"start": m[0], "end": m[1], "text": cleaned_text})
    storage.delete(video_path)
    storage.delete(subtitle_path)

    with ClosedCaption.batch_write() as batch:
        for subtitle in subtitles:
            batch.save(
                ClosedCaption(
                    videoId=video_file_hash,
                    caption=subtitle["text"],
                    startTime=subtitle["start"],
                    endTime=subtitle["end"],
                    url=file_url,
                )
            )
