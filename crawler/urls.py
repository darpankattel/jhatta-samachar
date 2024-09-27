from django.urls import path
from .views import EkantipurCrawler

# appended with /api/crawl/
urlpatterns = [
    path('ekantipur/', EkantipurCrawler.as_view(), name='crawl-news'),
]
