from django.contrib import admin
from .models import NewsArticles, Comment, Organizations, UserProfile
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(NewsArticles)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at')
    search_fields = ['title', 'author']
    list_filter = ('created_at', 'author')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('news_article', 'commenter', 'created_at')
    list_filter = ('news_article', 'created_at')
    search_fields = ('news_article__title', 'commenter__username', 'content') 
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    summernote_fields = ('content',)

@admin.register(Organizations)
class OrganizationAdmin(SummernoteModelAdmin):
    list_display = ('name', 'country', 'foundation')
    list_filter = ('country', 'foundation')
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    summernote_fields = ('description',)

@admin.register(UserProfile)
class UserProfileAdmin(SummernoteModelAdmin):
    list_display = ('user', 'account_opened', 'affiliated')
    list_filter = ('account_opened', 'affiliated')  
    search_fields = ('name', 'surname', 'email', 'username', 'affiliated')
    actions = ('approve_affiliated',)

    def approve_affiliated(self, request, queryset):
        queryset.update(active=True)