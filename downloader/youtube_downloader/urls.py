
from django.urls import path
from .views import download_video, download

urlpatterns = [
    path('', download_video, name='home'),
    path('download/', download, name='download'),
]
