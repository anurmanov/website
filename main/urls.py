from django.conf.urls import url
from django.views.decorators.cache import never_cache
from main.views import MainPageView, getRandomSliderImages

urlpatterns = [
    url('slider_images', getRandomSliderImages, name="slider_images"),
    url('', never_cache(MainPageView.as_view()), name="main"),
]