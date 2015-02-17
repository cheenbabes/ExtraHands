from django.conf.urls import patterns, url
from extra_hands_app import views

urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'teacher/(?P<teacher_slug>[\w\-]+)/$', views.get_teacher, name='get_teacher'),
url(r'teachers/$', views.get_all_teachers, name="get_all_teachers"),

)