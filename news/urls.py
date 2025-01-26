from django.urls import path
from .views import all_news, detail_news, ReadLater, UserProfileDetailView, OrganizationListView, OrganizationDetailView

urlpatterns = [
    path('', all_news, name='news_list'),
    path('read-later/', ReadLater.as_view(), name='read_later'),
    path('profile/<str:username>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('organizations/', OrganizationListView, name='organizations_list'),
    path('organizations/<slug:slug>/', OrganizationDetailView, name='organization_detail'),
    path('<slug:slug>/', detail_news, name='news_detail'),
]