from django.conf.urls import url

from . import views

app_name = 'video'
urlpatterns = [
    url(r'^search/', views.search, name='search'),
    url(r'^1/', views.get_and_save_item_from_youtube, name='get_and_save'),
    url(r'^next/', views.next_page_view, name='next_page'),
    url(r'^prev/', views.prev_page_view, name='prev_page'),
]
