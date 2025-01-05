from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import News
from .forms import CommentForm
# Create your views here.


class NewsList(generic.ListView):
    queryset = News.objects.all()
    template_name = "news/news_list.html"
    paginate_by = 12

class NewsDetail(generic.DetailView):
    model = News
    template_name = "news/news_detail.html"