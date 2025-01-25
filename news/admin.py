from django.contrib import admin
from .models import News, Comment, Organization
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at')
    search_fields = ['title', 'author']
    list_filter = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('news', 'commenter', 'created_at')
    list_filter = ('created_at', 'news')
    search_fields = ('news__title', 'commenter__username', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    summernote_fields = ('content',)

@admin.register(Organization)
class OrganizationAdmin(SummernoteModelAdmin):
    list_display = ('name', 'country', 'founded', 'rating')
    list_filter = ('country', 'founded')
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    filter_horizontal = ('subscribers', 'authors')
    summernote_fields = ('description',)