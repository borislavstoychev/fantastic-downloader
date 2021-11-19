from wsgiref.util import FileWrapper
import requests
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect
from pytube import YouTube
from django.core.files.temp import NamedTemporaryFile
from downloader.youtube.forms import DownloadForm


def download_video(request):
    if request.method == "POST":
        file = request.POST['download']
        video = YouTube(file).streams.get_highest_resolution()
        response = HttpResponse(video.url, content_type='video/mp4')
        response['Content-Disposition'] = f"attachment; filename={video.title}"
        response['Content-Length'] = video.filesize

        return response


def download_audio(request):
    if request.method == "POST":
        file = request.POST['download']
        audio = YouTube(file).streams.get_audio_only()
        response = FileResponse(audio.url, content_type='video/mp4', as_attachment=True, filename=audio.title)
        response['Content-Disposition'] = f"attachment; filename={audio.title}"
        response['Content-Length'] = audio.filesize

        return response


def video_view(request):
    videos = []

    if request.method == 'POST':
        form = DownloadForm(request.POST)
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        form.is_valid()
        search_params = {
            'part': 'snippet',
            'q': form.cleaned_data['url'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 21,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 21
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
            }

            videos.append(video_data)
    else:
        return render(request, 'youtube_search.html', {'form': DownloadForm()})

    context = {
        'videos': videos,
        'form': DownloadForm()
    }

    return render(request, 'youtube_search.html', context)
