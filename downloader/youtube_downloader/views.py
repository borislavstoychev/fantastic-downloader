import re
from django import views
from pytube import YouTube
from django.http import HttpResponse
from django.shortcuts import render
from .forms import DownloadForm


def get_context(url):
    ytb = YouTube(url)
    video_streams = ytb.streaming_data["formats"][-1]
    audio_streams = ytb.streaming_data['adaptiveFormats'][-4]
    context = {
        'form': DownloadForm(),
        'title': ytb.title,
        'video_resolution': f"{video_streams['width']}x{video_streams['height']}",
        "video_type": 'video/mp4',
        'video_streams_size': "Currently not available!",
        'description': ytb.description,
        'rating': ytb.rating,
        'views': ytb.views,
        'thumb': ytb.thumbnail_url,
        'author': ytb.author,
        'audio_type': 'audio/mp4',
        'audio_stream_size': "Currently not available!",
        'download': video_streams['url'] + "&title=" + ytb.title,
        'download_audio': audio_streams['url'] + "&title=" + ytb.title,

    }
    return context


def download_search(request):
    if request.method == "POST":
        url = request.POST['download']
        return render(request, 'home.html', get_context(url))
    return render(request, 'home.html', {'form': DownloadForm()})


# def download_home(request):
#     form = DownloadForm(request.POST)
#     if form.is_valid():
#         video_url = form.cleaned_data['url']
#         if not re.match(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+', video_url):
#             return HttpResponse('Enter correct url.')
#         return render(request, 'home.html', get_context(video_url))
#     return render(request, 'home.html', {'form': DownloadForm()})
