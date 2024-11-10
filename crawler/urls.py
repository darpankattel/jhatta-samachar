from django.urls import path
from .views import EkantipurCrawler, EkantipurRecursiveCrawler, CrawlAndSave

# appended with /api/crawl/
urlpatterns = [
    path('ekantipur/', EkantipurCrawler.as_view(), name='crawl-news'),
    path('recursive/ekantipur/', EkantipurRecursiveCrawler.as_view(),
         name='crawl-news-recursive'),
    path('', CrawlAndSave.as_view(),
         name='crawl'),
]
