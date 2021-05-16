from django.urls import path
from .views import Homepage, ArchivesView
urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('archives', ArchivesView.as_view(), name='archives')
]