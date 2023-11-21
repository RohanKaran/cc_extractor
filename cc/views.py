import boto3
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .forms import CCForm, SearchForm
from .models import ClosedCaption, Video
from .tasks import run_ccextractor


def upload_video(request):
    videos = Video.objects.all()
    if request.method == "POST":
        form = CCForm()
        search_form = SearchForm()
        action = request.POST.get("action")
        if action == "upload":
            form = CCForm(request.POST, request.FILES)
            file = request.FILES["file"]
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            s3_client.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                file.name,
                ExtraArgs={"ACL": settings.AWS_DEFAULT_ACL},
            )
            s3_file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file.name}"
            messages.success(
                request, "Upload successful! Your file URL is: " + s3_file_url
            )
            file.seek(0)
            storage = FileSystemStorage()
            storage.save(file.name, file)
            run_ccextractor.delay(storage.path(file.name), s3_file_url)
            return render(
                request,
                "main.html",
                {"form": form, "search_form": search_form, "videos": videos},
            )
        elif action == "search":
            search_form = SearchForm(request.POST)
            search = search_form.data["search"]
            videoId = search_form.data["videoId"]
            search_results = ClosedCaption.query(
                hash_key=videoId,
                filter_condition=ClosedCaption.caption.contains(search),
            )
            print(search_results)
            return render(
                request,
                "main.html",
                {
                    "search_form": search_form,
                    "search_results": search_results,
                    "form": form,
                    "videos": videos,
                },
            )
        else:
            return render(
                request,
                "main.html",
                {"form": form, "search_form": search_form, "videos": videos},
            )
    else:
        form = CCForm()
        search_form = SearchForm()
    return render(
        request,
        "main.html",
        {"form": form, "search_form": search_form, "videos": videos},
    )
