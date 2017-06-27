from django.conf.urls import url
from . import views
app_name = 'travels'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^add$', views.addpage, name='addpage'),
    url(r'^addthis$', views.addthis, name='addthis'),
    url(r'^join/(?P<id>\d+)$', views.join, name='join')
]
