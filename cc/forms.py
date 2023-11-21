from django import forms

from cc.models import Video


class CCForm(forms.Form):
    file = forms.FileField()


class SearchForm(forms.Form):
    videoId = forms.RadioSelect(choices=[video.videoId for video in Video.objects.all()])
    search = forms.CharField(max_length=100)
