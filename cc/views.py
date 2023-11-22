import boto3
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .forms import CCForm, SearchForm
from .models import ClosedCaption, Video
from .tasks import run_ccextractor


def main(request):
    videos = Video.objects.all()
    form = CCForm()
    search_form = SearchForm()
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "upload":
            form = CCForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, "Invalid form.")
                return redirect("main")
            file = request.FILES["file"]
            storage = FileSystemStorage()
            storage.save(file.name, file)
            file.seek(0)
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
                request,
                "Upload successful! Your file URL is: "
                + s3_file_url
                + ". "
                + "Refresh the page to see your video.",
            )
            run_ccextractor.delay(storage.path(file.name), s3_file_url)
            return redirect("main")
        elif action == "search":
            search_form = SearchForm(request.POST)
            if not search_form.is_valid():
                messages.error(request, "Invalid form.")
                return redirect("main")
            search = search_form.data["search"]
            videoId = search_form.data["videoId"]
            search_results = ClosedCaption.query(
                hash_key=videoId,
                filter_condition=ClosedCaption.caption.contains(search),
            )
            search_results = [result.attribute_values for result in search_results]
            request.session["search_results"] = search_results
            return redirect("main")
        else:
            messages.error(request, "Invalid form.")
            return redirect("main")

    else:
        search_results = request.session.get("search_results")
        if search_results:
            del request.session["search_results"]
        else:
            search_results = []
    print(search_results)
    return render(
        request,
        "main.html",
        {"videos": videos, "form": form, "search_form": search_form, "search_results": search_results},
    )
