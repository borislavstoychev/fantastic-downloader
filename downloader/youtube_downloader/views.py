import re
from pytube import YouTube
from django.http import HttpResponse
from django.shortcuts import render
from django.http import FileResponse
from django.utils.encoding import smart_str
from .forms import DownloadForm


def download_video(request):
    global context
    form = DownloadForm(request.POST)
    if form.is_valid():
        video_url = form.cleaned_data['url']
        if not re.match(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+', video_url):
            return HttpResponse('Enter correct url.')
        video = YouTube(video_url)
        video_streams = video.streams.get_highest_resolution()
        audio_streams = video.streams.get_audio_only()
        context = {
            'form': DownloadForm(),
            'title': video.title,
            'video_streams': video_streams,
            'video_streams_size': video_streams.filesize/1048576,
            'description': video.description,
            'rating': video.rating,
            'views': video.views,
            'thumb': video.thumbnail_url,
            'author': video.author,
            'audio_stream': audio_streams,
            'audio_stream_size': audio_streams.filesize/1048576,
            'download': video_streams.url + "&title=" + video.title,
            'download_audio': audio_streams.url + "&title=" + video.title,

        }

        return render(request, 'home.html', context)

    return render(request, 'home.html', {'form': form})


# def download(request, pk):
#     file =
#     response = FileResponse(open(file.download(), 'rb'), as_attachment=True, filename=title)
#     return response

