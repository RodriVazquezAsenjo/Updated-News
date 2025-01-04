from django.shortcuts import render
from django.views import generic
from .models import News
# Create your views here.


class NewsList(generic.ListView):
    queryset = News.objects.all()
    template_name = "news_list.html"
    paginate_by = 12

class NewsDetail(generic.DetailView) :
    queryset = News.objects.filter()
    template_name = "news_detail.html"


