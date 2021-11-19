from django.urls import path
from . import views

urlpatterns = [
    path('video-search/', views.video_view, name='search'),
]