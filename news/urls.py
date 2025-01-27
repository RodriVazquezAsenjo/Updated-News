from django.urls import path
from .views import all_news, detail_news, toggle_read_later, add_article, add_organization, profile_modifications, ReadLater, UserProfileDetailView, OrganizationListView, OrganizationDetailView

urlpatterns = [
    path('', all_news, name='news_list'),
    path('add_article/', add_article, name='add_article'),
    path('read-later/', ReadLater.as_view(), name='read_later'),
    path('profile/<str:username>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('profile/<str:username>/edit/', profile_modifications, name='profile_modifications'),
    path('organizations/', OrganizationListView, name='organizations_list'),
    path('organizations/<slug:slug>/', OrganizationDetailView, name='organization_detail'),
    path('add_organization/', add_organization, name='add_organization'),
    path('<slug:slug>/', detail_news, name='news_detail'),
    path('toggle-read-later/', toggle_read_later, name='toggle_read_later'),
]