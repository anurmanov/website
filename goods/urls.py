from django.conf.urls import url
from django.views.decorators.cache import never_cache
from goods.views import GoodsPageView, GoodDetailPageView, GoodCreateView, GoodUpdateView, CategoryListView, category_menu
from tinymce.views import spell_check, filebrowser, css, spell_check_callback

urlpatterns = [
    url(r'^(?:(?P<pk>\d+)/)?$', never_cache(GoodsPageView.as_view()), name="goods"),
    url(r'^(?P<pk>\d+)/detail/$', never_cache(GoodDetailPageView.as_view()), name="goods_detail"),
    url(r'^(?P<pk>\d+)/add/$', GoodCreateView.as_view(), name="goods_add"),
    url(r'^(?P<pk>\d+)/edit/$', GoodUpdateView.as_view(), name="goods_edit"),
    url(r'category_list', CategoryListView.as_view(), name="category_list"),
    url(r'category_menu', category_menu, name="category_menu"),
    url(r'^spellchecker/$', spell_check, name='tinymce-spellchecker'),
    url(r'^filebrowser/$', filebrowser, name='tinymce-filebrowser'),
    url(r'^tinymce4.css', css, name='tinymce-css'),
    url(r'^spellcheck-callback.js', spell_check_callback, name='tinymce-spellcheck-callback')
]