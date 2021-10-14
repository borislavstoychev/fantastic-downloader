
from django.urls import path
from .views import download_home, download_search

urlpatterns = [
    path('', download_home, name='home'),
    path('download/', download_search, name='download'),
]
