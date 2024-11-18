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
                # summary = news_soup.find(
                #     'meta', {'name': 'description'}).get('content', None)
                keywords = news_soup.find(
                    'meta', {'name': 'keyword'}).get('content', None)
                og_image_url = news_soup.find(
                    'meta', {'property': 'og:image'}).get('content', None)

                content = '\n'.join([p.get_text() for p in news_soup.select(
                    'div.description.current-news-block p')])

                category_slug = re.search(
                    pattern, news_link).group("category_slug")
                category_name = category_slug.replace(
                    "-", " ").replace("_", " ").title()

                category, created = Category.objects.get_or_create(
                    slug=category_slug,
                    defaults={
                        "name": category_name,
                        "description": f"News in {category_name} category"
                    }
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
                        # "summary": summary,
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


class EkantipurRecursiveCrawler(APIView):
    """
    Recursively crawls the website `https://ekantipur.com/en/` for news articles in a predefined category and stores
    the relevant data in the database. Provides an option to download the data as a CSV file.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.base_url = "https://ekantipur.com/"
        self.visited_links = set()
        self.news_data = []
        self.max_links_to_crawl = 200  # Set a limit to avoid infinite recursion
        self.predefined_category = "sports"  # The category we want to scrape

    def get(self, request, *args, **kwargs):
        starting_url = self.base_url + self.predefined_category
        # Limit depth to prevent infinite recursion
        self.recursive_crawl(starting_url, depth=20)

        # Save the collected news to the database
        self.save_to_database()

        # Provide CSV download link (could be via another API, or generated here)
        if request.GET.get("download_csv", True):
            return self.download_as_csv()

        messages.success(
            request, 'Crawling and population completed successfully.')
        return redirect('/admin/news/news/')

    def recursive_crawl(self, url, depth, def_response=None):
        if len(self.news_data) >= self.max_links_to_crawl or depth <= 0:
            return

        if url in self.visited_links:
            return

        if def_response is None:
            response = requests.get(url)
        else:
            response = def_response

        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            return

        self.visited_links.add(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all news links in the current page
        links = soup.find_all("a", href=True)
        pattern = rf"https://ekantipur.com/en/{self.predefined_category}/(?P<year>\d{{4}})/(?P<month>\d{{2}})/(?P<day>\d{{2}})/(?P<news_slug>[\w-]+)"
        print(f"Found {len(links)} links in {url}")
        for link in links:
            link_text = "/en" + \
                link['href'] if link['href'].startswith("/") else link['href']
            print(f"Processing {link['href']}")
            full_url = urljoin(
                self.base_url, link_text)
            if re.match(pattern, full_url) and full_url not in self.visited_links:
                def_response = self.scrape_news(full_url)
                # Recursive call to crawl inside the links
                self.recursive_crawl(full_url, depth - 1, def_response)
            else:
                print(f"Skipping {full_url}")

    def scrape_news(self, news_url):
        try:
            news_response = requests.get(news_url)
            if news_response.status_code != 200:
                print(f"Failed to retrieve {news_url}")
                return

            news_soup = BeautifulSoup(news_response.content, "html.parser")
            title = news_soup.find("h1").text.strip(
            ) if news_soup.find("h1") else None
            content = '\n'.join([p.get_text() for p in news_soup.select(
                'div.description.current-news-block p')])
            summary = news_soup.find(
                'meta', {'name': 'description'}).get('content', None)
            keywords = news_soup.find(
                'meta', {'name': 'keyword'}).get('content', None)
            og_image_url = news_soup.find(
                'meta', {'property': 'og:image'}).get('content', None)

            # Extract published date from the URL
            published_at_match = re.search(
                r"(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})", news_url)
            published_at = "-".join(published_at_match.groups()
                                    ) if published_at_match else timezone.now().date()

            news_item = {
                "source_url": news_url,
                "title": title,
                "summary": summary,
                "content": content,
                "keywords": keywords,
                "og_image_url": og_image_url,
                "category": self.predefined_category,
                "published_at": published_at
            }
            if news_item not in self.news_data and news_item["title"]:
                self.news_data.append(news_item)
            return news_response

        except Exception as e:
            print(f"Failed to scrape {news_url}: {str(e)}")

    def save_to_database(self):
        print(f"Saving {len(self.news_data)} news articles to the database.")
        print(self.news_data)
        for news in self.news_data:
            category, created = Category.objects.get_or_create(
                name=self.predefined_category.title(),
                defaults={
                    "description": f"News in {self.predefined_category.title()} category"}
            )
            News.objects.get_or_create(
                source_url=news['source_url'],
                title=news['title'],
                defaults={
                    "content": news['content'],
                    "summary": news['summary'],
                    "keywords": news['keywords'],
                    "og_image_url": news['og_image_url'],
                    "category": category,
                    "published_at": news['published_at']
                }
            )
        print(f"Saved {len(self.news_data)} news articles to the database.")

    def download_as_csv(self):
        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="js_news_ek_{self.predefined_category}.csv"'

        writer = csv.writer(response)
        writer.writerow(["Source URL", "Title", "Summary",
                        "Content", "Keywords", "OG Image URL", "Category", "Published At"])

        for news in self.news_data:
            writer.writerow([
                news['source_url'],
                news['title'],
                news['summary'],
                news['content'],
                news['keywords'],
                news['og_image_url'],
                news['category'],
                news['published_at']
            ])

        return response


class CrawlAndSave(APIView):
    def get(self, request, *args, **kwargs):
        def_category = "feature"
        news_data = []
        from crawler.data import myset
        news_links = myset

        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="js_news_ek_{def_category}.csv"'

        writer = csv.writer(response)
        writer.writerow(["Source_URL", "Title", "Summary",
                        "Content", "Keywords", "OG_Image_URL", "Category", "Published_At"])

        for i, link in enumerate(news_links):
            print(f"Processing {i+1}/{len(news_links)}, {link}", end=" ")
            link = link.lower()
            if not link.startswith("https://ekantipur.com"):
                news_url = "/en" + link
                news_url = urljoin("https://ekantipur.com", news_url)
            else:
                news_url = link.replace(
                    "https://ekantipur.com", "https://ekantipur.com/en")

            print(f"-----> {news_url}", end=" ")

            pattern = rf"https://ekantipur.com/en/{def_category}/(?P<year>\d{{4}})/(?P<month>\d{{2}})/(?P<day>\d{{2}})/(?P<news_slug>[\w-]+)"

            if not re.match(pattern, news_url):
                print(f" SKIPPING...")
                continue

            news_response = requests.get(news_url)
            if news_response.status_code != 200:
                print(f"ERROR: Failed to retrieve")
                continue

            news_soup = BeautifulSoup(news_response.content, "html.parser")

            title = news_soup.find("h1").text.strip(
            ) if news_soup.find("h1") else None
            content = '\n'.join([p.get_text() for p in news_soup.select(
                'div.description.current-news-block p')])
            summary = news_soup.find(
                'meta', {'name': 'description'}).get('content', None)
            keywords = news_soup.find(
                'meta', {'name': 'keyword'}).get('content', None)
            og_image_url = news_soup.find(
                'meta', {'property': 'og:image'}).get('content', None)

            # Extract published date from the URL
            published_at_match = re.search(
                r"(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})", news_url)
            published_at = "-".join(published_at_match.groups()
                                    ) if published_at_match else timezone.now().date()

            news_item = {
                "source_url": news_url,
                "title": title,
                "summary": summary,
                "content": content,
                "keywords": keywords,
                "og_image_url": og_image_url,
                "category": def_category.title(),
                "published_at": published_at
            }
            if news_item not in news_data and news_item["title"]:
                news_data.append(news_item)

                category, created = Category.objects.get_or_create(
                    name=def_category.title(),
                    defaults={
                        "description": f"News in {def_category.title()} category"}
                )
                try:
                    News.objects.get_or_create(
                        source_url=news_item['source_url'],
                        title=news_item['title'],
                        defaults={
                            "content": news_item['content'],
                            "summary": news_item['summary'],
                            "keywords": news_item['keywords'],
                            "og_image_url": news_item['og_image_url'],
                            "category": category,
                            "published_at": news_item['published_at']
                        }
                    )
                except Exception as e:
                    print(f"Failed to save {news_url}: {str(e)}")

                writer.writerow([
                    news_item['source_url'],
                    news_item['title'],
                    news_item['summary'],
                    news_item['content'],
                    news_item['keywords'],
                    news_item['og_image_url'],
                    news_item['category'],
                    news_item['published_at']
                ])
                print(" DONE")

        return response
