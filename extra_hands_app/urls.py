from django.conf.urls import patterns, url
from extra_hands_app import views

urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'teacher/(?P<teacher_slug>[\w\-]+)/$', views.get_teacher, name='get_teacher'),
url(r'teachers/$', views.get_all_teachers, name="get_all_teachers"),
url(r'client/(?P<client_slug>[\w\-]+)/$', views.get_client, name ='get_client'),
url(r'clients/$', views.get_all_clients, name="get_all_clients"),
url(r'client/(?P<client_slug>[\w\-]+)/add_event/$', views.add_event, name='add_event')

)