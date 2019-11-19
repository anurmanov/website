from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.base import TemplateView
from generic.mixins import PageNumberMixin
from news.models import News
from services.models import Service
from goods.models import Good
#from accomplishments.models import Accomplishment
from generic.mixins import CompanyInfoMixin

class SearchResultsView(PageNumberMixin, TemplateView, CompanyInfoMixin):
    template_name = 'search.html'
    paginated_by = 10
    def get(self, request, *args, **kwargs):
        self.text = request.GET.get('search_text','')
        return super(SearchResultsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['text'] = self.text
        #поиск по услугам
        qs = Service.objects.filter(Q(name__contains=context['text'])|Q(description__contains=context['text']))
        c1 = [{'name': q.name, 'description': q.description, 'url': q.get_absolute_url()} for q in qs]
        #поиск по новостям
        qs = News.objects.filter(Q(name__contains=context['text'])|Q(content__contains=context['text']))
        c2 = [{'name': q.name, 'description': '...содержание новости', 'url': q.get_absolute_url()} for q in qs]
        #поиск по товарам
        qs = Good.objects.filter(Q(name__contains=context['text'])|Q(content__contains=context['text'])|Q(manufacturer__name__contains=context['text']))
        c3 = [{'name': q.name, 'description': '...описание товара', 'url': q.get_absolute_url()} for q in qs]
        ##поиск по достижениям
        #qs = Accomplishment.objects.filter(Q(name__contains=context['text'])|Q(description__contains=context['text']))
        #c4 = [{'name': q.name, 'description': q.description, 'url': q.get_absolute_url()} for q in qs]

        #results = [{'result_index': c[0], 'value': c[1]} for c in list(enumerate(c1 + c2 + c3 + c4, 1))]
        results = [{'result_index': c[0], 'value': c[1]} for c in list(enumerate(c1 + c2 + c3, 1))]

        paginator = Paginator(results, self.paginated_by)
        try:
            search_results = paginator.page(context['pn'])
        except EmptyPage:
            search_results = paginator.page(1)
        if paginator.num_pages > 1:
            context['is_paginated'] = True
        else:
            context['is_paginated'] = False
        context['paginator'] = paginator
        context['page_obj'] = search_results
        context['results'] = search_results
        return context
