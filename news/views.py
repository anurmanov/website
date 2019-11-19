from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from generic.mixins import PageNumberMixin
from news.models import News
from generic.mixins import CompanyInfoMixin

class NewsPageView(PageNumberMixin, ListView, CompanyInfoMixin):
    template_name = 'news.html'
    model = News
    paginate_by = 10

class NewsItemPageView(PageNumberMixin, DetailView, CompanyInfoMixin):
    template_name = 'news_item.html'
    model = News
    def get(self, request, *args, **kwargs):
        return super(NewsItemPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewsItemPageView, self).get_context_data(**kwargs)
        return context

