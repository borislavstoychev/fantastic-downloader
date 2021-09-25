from django import forms


class DownloadForm(forms.Form):
    url = forms.URLField(widget=forms.TextInput(attrs={ 'placeholder': 'Enter video url' }), label=False)
