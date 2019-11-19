from django.conf.urls import url
from search.views import SearchResultsView

urlpatterns = [
    url(r'.*', SearchResultsView.as_view(), name="search"),
]