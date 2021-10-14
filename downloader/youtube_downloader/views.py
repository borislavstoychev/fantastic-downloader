import re
from pytube import YouTube
from django.http import HttpResponse
from django.shortcuts import render
from .forms import DownloadForm


def get_context(url):
    ytb = YouTube(url)
    video_streams = ytb.streams.get_highest_resolution()
    audio_streams = ytb.streams.get_audio_only()
    context = {
        'form': DownloadForm(),
        'title': ytb.title,
        'video_streams': video_streams,
        'video_streams_size': video_streams.filesize / 1048576,
        'description': ytb.description,
        'rating': ytb.rating,
        'views': ytb.views,
        'thumb': ytb.thumbnail_url,
        'author': ytb.author,
        'audio_stream': audio_streams,
        'audio_stream_size': audio_streams.filesize / 1048576,
        'download': video_streams.url + "&title=" + ytb.title,
        'download_audio': audio_streams.url + "&title=" + ytb.title,

    }
    return context


def download_home(request):
    form = DownloadForm(request.POST)
    if form.is_valid():
        video_url = form.cleaned_data['url']
        if not re.match(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+', video_url):
            return HttpResponse('Enter correct url.')
        return render(request, 'home.html', get_context(video_url))
    return render(request, 'home.html', {'form': DownloadForm()})


def download_search(request):
    if request.method == "POST":
        url = request.POST['download']
        return render(request, 'home.html', get_context(url))
    return render(request, 'home.html', {'form': DownloadForm()})


