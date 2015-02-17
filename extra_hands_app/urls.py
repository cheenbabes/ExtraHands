from django.conf.urls import patterns, url
from extra_hands_app import views

urlpatterns = patterns('',
url(r'^$', views.index, name='index'),

)