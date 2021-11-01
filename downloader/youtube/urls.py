from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_view, name='home'),
    path('download/', views.download_audio, name='audio'),
    path('video/', views.download_video, name="video")
]
