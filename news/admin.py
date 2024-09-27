from django.contrib import admin
from .models import News, Category
from crawler.admin import CrawlNewsAdmin

admin.site.register(Category)
admin.site.register(News, CrawlNewsAdmin)
