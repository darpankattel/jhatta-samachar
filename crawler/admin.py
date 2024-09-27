from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.conf import settings


class CrawlNewsAdmin(admin.ModelAdmin):
    change_list_template = "admin/crawl_ekantipur.html"  # Custom template

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('crawl-ekantipur/', self.admin_site.admin_view(self.crawl_ekantipur),
                 name='crawl-ekantipur'),
        ]
        return custom_urls + urls

    def crawl_ekantipur(self, request):
        # Redirect to the /api/crawl/ekantipur/ endpoint when the button is clicked
        return HttpResponseRedirect('/api/crawl/ekantipur/')

    def crawl_ekantipur_button(self, obj):
        return format_html('<a class="button" href="{}">Crawl Ekantipur</a>', "/admin/crawl-ekantipur/")

    crawl_ekantipur_button.short_description = "Crawl Ekantipur"
    crawl_ekantipur_button.allow_tags = True


admin.site.site_header = "Jhatta Samachar Admin Panel"
admin.site.site_title = "Jhatta Samachar Admin Panel"
admin.site.index_title = "Welcome to Jhatta Samachar Admin Panel"
