import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from news.models import News, Category
from urllib.parse import urljoin
import re
from django.contrib import messages
from django.shortcuts import redirect
# django default authenticatino class
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class EkantipurCrawler(APIView):
    """
    Crawls the website `https://ekantipur.com/en/` for english news articles and stores the relevant data in the database.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        base_url = "https://ekantipur.com/"
        pattern = r"https://ekantipur.com/en/(?P<category_slug>[\w-]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<news_slug>[\w-]+)"

        response = requests.get(base_url)
        if response.status_code != 200:
            messages.error(request, "Failed to retrieve the website content.")
            return redirect('/admin/news/news/')

        soup = BeautifulSoup(response.content, "html.parser")

        # TODO: Implement the crawling logic recursively, it is currently only crawling the first page.
        all_links = soup.find_all('a', href=True)
        news_links = set()

        for link in all_links:
            href = link['href']
            full_url = urljoin(base_url + "en/", href)

            if re.match(pattern, full_url):
                news_links.add(full_url)

        print(f"Found {len(news_links)} news articles.")

        for i, news_link in enumerate(news_links):
            try:
                news_response = requests.get(news_link)
                if news_response.status_code != 200:
                    continue

                news_soup = BeautifulSoup(news_response.content, "html.parser")

                title = news_soup.find("h1").text.strip(
                ) if news_soup.find("h1") else None
                # TODO: comment the summary, as we will generating it from the content
                summary = news_soup.find(
                    'meta', {'name': 'description'}).get('content', None)
                keywords = news_soup.find(
                    'meta', {'name': 'keyword'}).get('content', None)
                og_image_url = news_soup.find(
                    'meta', {'property': 'og:image'}).get('content', None)

                content = '\n'.join([p.get_text() for p in news_soup.select(
                    'div.description.current-news-block p')])

                category_slug = re.search(
                    pattern, news_link).group("category_slug")
                category_name = category_slug.replace("-", " ").title()

                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={
                        "description": f"News in {category_name} category"}
                )

                published_at = re.search(
                    pattern, news_link).group("year", "month", "day")
                published_at = "-".join(published_at)
                if not published_at:
                    # only date
                    published_at = timezone.now().date()
                News.objects.get_or_create(
                    source_url=news_link,
                    defaults={
                        "source_name": "Ekantipur",
                        "keywords": keywords,
                        "og_image_url": og_image_url,
                        "title": title,
                        "content": content,
                        "summary": summary,
                        "category": category,
                        "published_at": published_at
                    }
                )
                print(f"Processed {i+1}/{len(news_links)} news articles.")

            except Exception as e:
                print(
                    f"Failed to process {i+1}/{len(news_links)}. {news_link}: {str(e)}")

        messages.success(
            request, 'Crawling and population completed successfully.')
        return redirect('/admin/news/news/')
