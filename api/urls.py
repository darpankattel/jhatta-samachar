from django.urls import path, include

urlpatterns = [
    path('news/', include('news.urls')),
    path('auth/', include('account.urls')),
    path('crawl/', include('crawler.urls')),
]
