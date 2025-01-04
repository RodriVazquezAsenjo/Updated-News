from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique = True, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="news_articles"
    )
    likes = models.PositiveIntegerField(default=0)
    read_later_by = models.ManyToManyField(User, related_name='read_later_news', blank=True)

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"