from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Organizations(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    foundation = models.DateField(null=True, blank=True)
    country = CountryField()

    def __str__(self):
        return self.name

    def total_authors(self):
        return self.affiliated_users.count()

    class Meta:
        ordering = ['name']


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    affiliated = models.ForeignKey(
        Organizations, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='affiliated_users'
    )
    nationality = CountryField()
    account_opened = models.DateTimeField(auto_now_add=True)
    subscriber = models.ManyToManyField(
        'self', 
        symmetrical=False,
        blank=True,
        related_name='subscribers'
    )

    def __str__(self):
        return self.user.username

    def subscriber_count(self):
        return self.subscriber.count()


class NewsArticles(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='author'
    )
    likes = models.ManyToManyField(
        UserProfile,
        related_name='like',
        blank=True
    )
    bookmark = models.ManyToManyField(
        UserProfile,
        related_name='bookmark',
        blank=True,
    )
    organization = models.ForeignKey(
        Organizations, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='organization'
    )

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
    
    def total_comments(self):
        return self.comments.count()

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    news_article = models.ForeignKey(
        NewsArticles,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    commenter = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='commenter'
    )

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.commenter.username)


    class Meta:
        ordering = ["-created_at"]