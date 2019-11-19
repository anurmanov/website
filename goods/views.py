from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import UpdateView
from generic.mixins import PageNumberMixin
from goods.models import Good, Category
from django import forms
from tinymce import TinyMCE
from generic.mixins import CompanyInfoMixin
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache, caches
from django.core.serializers import serialize, deserialize
from django.conf import settings
from visits.generic.count_visitors import count_visitors

from rest_framework.generics import ListAPIView
from rest_framework.serializers import Serializer
from .serializers import CategorySerializer

class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = '__all__'
    content = forms.CharField(label = 'Описание', widget=TinyMCE())


class GoodsPageView(PageNumberMixin, ListView, CompanyInfoMixin):
    model = Good
    template_name = 'goods.html'
    paginated_by = 10
    cat = None
    @count_visitors
    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] == None:
            self.cat = None
        else:
            self.cat = Category.objects.get(pk = self.kwargs['pk'])
        return super(GoodsPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodsPageView, self).get_context_data(**kwargs)
        if self.cat:
            context['ancestors'] = self.cat.ancestors()
        else:
            context['ancestors'] = [None, ]
        #key = 'subgroups:' + (str(self.cat.id) if self.cat else 'parent')
        #if key in cache:
        #    context['subgroups'] =  deserialize('json', cache.get(key))
        #else:
        #    context['subgroups'] = Category.objects.filter(parent_category = self.cat)
        #    values = serialize('json', context['subgroups'])
        #    cache.set(key, values, timeout = 900)           
        context['subgroups'] = Category.objects.filter(parent_category = self.cat)
        context['category'] = self.cat
        context['goods'] = Good.objects.filter(category = self.cat)
        return context
    def get_queryset(self):
        goods = Good.objects.filter(category = self.cat)
        return goods

class GoodDetailPageView(PageNumberMixin, DetailView, CompanyInfoMixin):
    model = Good
    template_name = 'good.html'
    @count_visitors
    def get(self, request, *args, **kwargs):
        self.category = Good.objects.get(pk = self.kwargs['pk']).category
        return super(GoodDetailPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodDetailPageView, self).get_context_data(**kwargs)
        context['ancestors'] = self.category.ancestors()
        return context

class GoodCreateView(PageNumberMixin, TemplateView, CompanyInfoMixin):
    template_name = 'good_edit.html'
    cat = None
    form = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] == None:
            self.category = None
        else:
            self.category = Category.objects.get(pk = self.kwargs['pk'])
        self.form = GoodForm(initial = {'category': self.category})
        return super(GoodCreateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCreateView, self).get_context_data(**kwargs)
        context["form"] = self.form
        context['category'] = self.category
        context['ancestors'] = self.category.ancestors()
        context['form_caption'] = 'Добавить товар'
        context['header_caption'] = 'Добавить товар'
        context['submit_button_caption'] = 'Добавить'
        return context

    def post(self, request, *args, **kwargs):
        self.form = GoodForm(request.POST, request.FILES)
        if self.kwargs["pk"] == None:
            self.category = Category.objects.first()
        else:
            self.category = Category.objects.get(pk = self.kwargs["pk"])
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse("goods", kwargs = {"pk": self.category.pk}))
        return super(GoodCreateView, self).get(request, *args, **kwargs)

class GoodUpdateView(PageNumberMixin, UpdateView, CompanyInfoMixin):
    model = Good
    template_name = 'good_edit.html'
    fields = '__all__'
    good = None
    form = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] == None:
            self.good = None
        else:
            self.good = Good.objects.get(pk = self.kwargs['pk'])
        self.form = GoodForm(instance = self.good)
        return super(GoodUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodUpdateView, self).get_context_data(**kwargs)
        context["form"] = self.form
        context['category'] = self.good.category
        context['ancestors'] = self.good.category.ancestors()
        context['form_caption'] = 'Редактировать товар'
        context['header_caption'] = 'Редактировать товар'
        context['submit_button_caption'] = 'Сохранить'
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == None:
            self.good = None
        else:
            self.good = Good.objects.get(pk = self.kwargs['pk'])
        self.form = GoodForm(request.POST, request.FILES, instance = self.good)
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse("goods", kwargs = {"pk": self.good.category.pk}))
        return super(GoodUpdateView, self).get(request, *args, **kwargs)

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        objs = Category.objects.all()
        for ob in objs:
            if ob.parent_category:
                ob.parent_name = ob.parent_category.name
            else:
                ob.parent_name = ''
        return objs

def category_menu(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            data = {}
            cats = Category.objects.filter(parent_category__isnull = True)
            for cat in cats:
                data[cat.name] = cat.build_child_tree()
            return JsonResponse(data)
        else:
            return HttpResponse(status = 401, content = '<h1>Unsufficient privileges for performing request!</h1>', charset = 'utf-8')
    else:
        return HttpResponseNotAllowed('<h1>Unsupported HTTP method!</h1>')

