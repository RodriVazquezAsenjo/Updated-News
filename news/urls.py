from django.urls import path
from .views import NewsList, NewsDetail, ReadLater, UserProfileDetailView

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('read-later/', ReadLater.as_view(), name='read_later'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile'),
    path('<slug:slug>/', NewsDetail.as_view(), name='news_detail'),
]