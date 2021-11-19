
from django.urls import path
from .views import download_search

urlpatterns = [
    path('', download_search, name='download'),
]
