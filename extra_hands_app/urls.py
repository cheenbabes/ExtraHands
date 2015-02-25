from django.conf.urls import patterns, url
from extra_hands_app import views

urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'teacher/(?P<teacher_slug>[\w\-]+)/$', views.get_teacher, name='get_teacher'),
url(r'teachers/$', views.get_all_teachers, name="get_all_teachers"),
url(r'client/(?P<client_slug>[\w\-]+)/$', views.get_client, name ='get_client'),
url(r'clients/$', views.get_all_clients, name="get_all_clients"),
url(r'client/(?P<client_slug>[\w\-]+)/add_event/$', views.add_event, name='add_event'),
url(r'register/teacher/$', views.register_teacher, name='register_teacher'),
url(r'register/client/$', views.register_client, name='register_client'),
url(r'login/$', views.user_login, name='login'),
url(r'logout/$', views.user_logout, name='logout'),
url(r'myaccount/$', views.my_account, name='myaccount'),
url(r'action/on-call/$', views.go_on_call, name='go_on_call')

)