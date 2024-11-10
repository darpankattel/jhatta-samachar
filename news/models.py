from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __save__(self, *args, **kwargs):
        self.slug = self.slug.lower()
        if self.slug and (not self.name):
            self.name = self.slug.replace("-", " ").replace("_", " ").title()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(null=True, blank=True)  # Summary of the article

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    # URL of the original news article
    source_url = models.URLField(unique=True, null=True, blank=True)
    # Name of the news source (e.g., 'BBC')
    source_name = models.CharField(max_length=255, null=True, blank=True)
    published_at = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    keywords = models.TextField(null=True, blank=True)
    og_image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_source(self):
        return self.source_name

    class Meta:
        verbose_name_plural = "All News"
        ordering = ['-published_at', '-updated_at', 'title']
