from django.contrib.auth.models import User
from django.db import models
from news.models import Category
from news.models import News


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    google_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)

    # Profile picture from Google
    picture = models.URLField(null=True, blank=True)

    likes = models.ManyToManyField(
        Category, related_name='liked_by', blank=True)
    dislikes = models.ManyToManyField(
        Category, related_name='disliked_by', blank=True)

    def __str__(self):
        return self.user.username

    def get_preferred_news(self):
        """
        Returns news articles based on user preferences.
        """
        liked_categories = self.likes.all()
        disliked_categories = self.dislikes.all()
        news = News.objects.all()
        if liked_categories:
            news = news.filter(category__in=liked_categories)
        if disliked_categories:
            news = news.exclude(category__in=disliked_categories)

        return news
