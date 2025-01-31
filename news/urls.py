from django.urls import path
from .views import all_news_articles, selected_news_article, add_article, add_organization, profile_modifications, profile_view, all_organizations, selected_organizations, like, bookmark

urlpatterns = [
    path('', all_news_articles, name='news_list'),
    path('add_article/', add_article, name='add_article'),
    path('profile/<str:username>/', profile_view, name='user_profile'),
    path('profile/<str:username>/edit/', profile_modifications, name='profile_modifications'),
    path('organizations/', all_organizations, name='organizations_list'),
    path('organizations/<slug:slug>/', selected_organizations, name='organization_detail'),
    path('add_organization/', add_organization, name='add_organization'),
    path('<slug:slug>/', selected_news_article, name='news_detail'),
    path('news_article/<int:pk>/', like, name='news_article_like'),
    path('news_article/<slug:slug>/bookmark/', bookmark, name='news_article_bookmark'),
    path('bookmark/', bookmark, name='bookmark')
]