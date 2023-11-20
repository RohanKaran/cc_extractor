from django import forms


class CCForm(forms.Form):
    file = forms.FileField(required=False)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)
