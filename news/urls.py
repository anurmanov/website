from django.conf.urls import url
from news.views import NewsPageView, NewsItemPageView
from tinymce.views import spell_check, filebrowser, css, spell_check_callback

urlpatterns = [
    url(r'^(?:(?P<pk>\d+)/)?$', NewsPageView.as_view(), name='news'),
    url(r'^(?P<pk>\d+)/detail/$', NewsItemPageView.as_view(), name='news_detail'),
    url(r'^spellchecker/$', spell_check, name='tinymce-spellchecker'),
    url(r'^filebrowser/$', filebrowser, name='tinymce-filebrowser'),
    url(r'^tinymce4.css', css, name='tinymce-css'),
    url(r'^spellcheck-callback.js', spell_check_callback, name='tinymce-spellcheck-callback')
]