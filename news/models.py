from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class News(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="news_articles"
    )
    likes = models.PositiveIntegerField(default=0)
    read_later_by = models.ManyToManyField(
        User,
        related_name='read_later_news',
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.news.title}"

    class Meta:
        ordering = ["-created_at"]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    account_opened = models.DateTimeField(auto_now_add=True)
    affiliation = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affiliated_users"
    )

    def __str__(self):
        return self.user.username


class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(unique=True)
    #logo = models.ImageField(null=True, blank=True)
    description = models.TextField()
    founded = models.DateField(null=True, blank=True)
    country = CountryField()
    subscribers = models.ManyToManyField(
        User,
        related_name='subscribed_organizations',
        blank=True
    )
    authors = models.ManyToManyField(
        User,
        related_name='authored_organizations',
        blank=True
    )
    rating = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rated_organizations'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ['name']