from django.contrib import admin
from .models import News
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at')
    search_fields = ['title', 'author']
    list_filter = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)