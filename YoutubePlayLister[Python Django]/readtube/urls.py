from django.urls import re_path
from readtube import views

urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view()),
    re_path(r'^Channels/$', views.ChannelPageView.as_view()),
]
