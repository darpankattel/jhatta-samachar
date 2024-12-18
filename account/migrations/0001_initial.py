# Generated by Django 4.2.16 on 2024-10-08 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('picture', models.URLField(blank=True, null=True)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='disliked_by', to='news.category')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_by', to='news.category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
