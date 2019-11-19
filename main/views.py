import os, sys, random, glob
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseNotAllowed
from generic.mixins import CompanyInfoMixin
from goods.models import Good
from visits.generic.count_visitors import count_visitors
from medsmartcom.settings import BASE_DIR

def getRandomSliderImages(request):
    if request.method == 'GET':
        sliders_dir_url = 'static/images/slider'
        sliders_dir =  os.path.join(BASE_DIR, sliders_dir_url)
        random_dir = random.choice([dir for dir in os.listdir(sliders_dir) if os.path.isdir(sliders_dir + '/' + dir)])
        files = map(os.path.basename, glob.glob(sliders_dir + '/' + random_dir + '/*.jpg')) #list(os.walk(sliders_dir + '/' + random_dir))[0][2]
        return JsonResponse(['/' + sliders_dir_url +'/' + random_dir + '/' + f for f in files], safe=False)
    else:
        return HttpResponseNotAllowed('<h1>Unsupported HTTP method!</h1>')

class MainPageView(TemplateView, CompanyInfoMixin):
    template_name = 'mainpage.html'
    @count_visitors
    def get(self, request, *args, **kwargs):
        return super(MainPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['featured_goods'] = Good.objects.filter(featured = True)
        return context

class AdminkaPageView(TemplateView):
    template_name = 'adminka.html'
