from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^postSecret$', views.postSecret), 
    url(r'^like/(?P<like_id>\d+)/(?P<user_id>\d+)$', views.like),
    url(r'^logout$', views.logout),
    url(r'^deletePost/(?P<id>\d+)$', views.delete),
    url(r'^unlike/(?P<like_id>\d+)/(?P<user_id>\d+)$', views.unlike),
    url(r'^mostPopular$', views.mostPopular)

]


