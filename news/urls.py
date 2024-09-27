from django.urls import path
from .views import NewsSummaryListView, SummarizeAllNewsView, NewsSummaryMP3View, NewsCategoryView

# appends with /api/news/
urlpatterns = [
    # for the news app
    path('', NewsSummaryListView.as_view(), name='news-summary-list'),
    path('mp3/', NewsSummaryMP3View.as_view(), name='news-summary-mp3'),
    path('category/', NewsCategoryView.as_view(), name='news-category'),

    # for admin control
    path('summarizeall/', SummarizeAllNewsView.as_view(), name='news-summarize'),
]
