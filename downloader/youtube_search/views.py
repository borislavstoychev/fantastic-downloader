import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect

from downloader.youtube_downloader.forms import DownloadForm


def video_view(request):
    videos = []
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            video_url = 'https://www.googleapis.com/youtube/v3/videos'

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

            if request.POST['submit'] == 'lucky':
                return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')

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

    context = {
        'videos': videos,
        'form': DownloadForm()
    }

    return render(request, 'youtube_search.html', context)
