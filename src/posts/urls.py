from django.conf.urls import url
#from django.contrib import admin
#from posts import views as post_views
#from posts import views as post_forms
from .views import (
    post_list,
    post_create,
    post_delete,
    post_detail,
    post_update
)

urlpatterns = [
    #url(r'^post/', <function_name>),
    url(r'^$', post_list, name= "list"),
    url(r'^create/$', post_create),        #post_create is a function in views.py
    url(r'^(?P<id>\d+)/$', post_detail, name="details"), #passing a parameter id helps in url searching http://joincfe.com/guides
    url(r'^(?P<id>\d+)/edit/$', post_update, name="update"),
    url(r'^(?P<id>\d+)/delete/$', post_delete),

]
