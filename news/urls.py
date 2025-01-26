from django.urls import path
from .views import all_news, detail_news, add_article, add_organization, ReadLater, UserProfileDetailView, OrganizationListView, OrganizationDetailView

urlpatterns = [
    path('', all_news, name='news_list'),
    path('add_article/', add_article, name='add_article'),
    path('read-later/', ReadLater.as_view(), name='read_later'),
    path('profile/<str:username>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('organizations/', OrganizationListView, name='organizations_list'),
    path('organizations/<slug:slug>/', OrganizationDetailView, name='organization_detail'),
    path('add_organization/', add_organization, name='add_organization'),
    path('<slug:slug>/', detail_news, name='news_detail'),
]