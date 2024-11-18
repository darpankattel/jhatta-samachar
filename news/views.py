from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from gtts import gTTS
import os
from django.http import HttpResponse, FileResponse
from rest_framework import generics, status
from .models import News, Category
from account.models import CustomUser
from .serializers import NewsSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from core.pagination import CustomPagination
# media
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect


class NewsSummaryListView(generics.ListAPIView):
    """
    Lists news articles with summaries based on user preferences. No real content is sent in the response.

    The view filters news articles based on the user's liked and disliked categories.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        custom_user = CustomUser.objects.get(user=user.id)

        # news_without_summary = custom_user.get_preferred_news().filter(
        #     Q(summary__isnull=True) | Q(summary='')
        # )

        # if news_without_summary.count() != 0:
        #     from .utils import get_news_summary
        #     for _news in news_without_summary:
        #         new_summary = get_news_summary(_news)
        #         _news.summary = new_summary
        #         _news.save()

        news = custom_user.get_preferred_news()

        return news


class NewsSummaryMP3View(APIView):
    """
    Generates an MP3 file containing a summary of the latest news articles.

    Paginated response is supported.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        custom_user = CustomUser.objects.get(user=user)
        news = custom_user.get_preferred_news()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(news, request)

        if page is not None:
            news = page

        text = "Let's start the news summary. " + " Now, Next News. ".join(
            [article.title + ". " + article.summary for article in news]) + ". That's all for now. Thank you for listening."

        # if paginator contains next page
        if paginator.get_next_link():
            text += " For more news, please press the next button."

        # Use gTTS to generate the MP3 file
        file_name = f"{settings.MEDIA_ROOT}/mp3/{user.id}-{request.GET.get('page', 1)}.mp3"
        if not os.path.exists(file_name):
            print("Converting!")
            tts = gTTS(text)
            tts.save(file_name)
            print(f"MP3 file saved at: {file_name}")
        # Serve the MP3 file as a response

        return FileResponse(open(file_name, "rb"), content_type="audio/mp3")
        return Response(status=status.HTTP_404_NOT_FOUND)


class NewsCategoryView(generics.ListAPIView):
    """
    Lists all news categories.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SummarizeAllNewsView(APIView):
    """
    Potential endpoint for summarizing the content of entire database.

    For admin use only.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        # try:
        news = News.objects.filter(Q(summary__isnull=True) | Q(summary=''))
        from .utils import get_news_summary
        for _news in news:
            new_summary = get_news_summary(_news)
            _news.summary = new_summary
            _news.save()
        messages.success(
            request, f"All {len(news)} news articles have been summarized.")
        return redirect('/admin/news/news/')
        # except Exception as e:
        #     messages.error(request, f"An error occurred: {str(e)}")
        #     return redirect('/admin/news/news/')
