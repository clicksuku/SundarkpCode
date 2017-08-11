from django.conf.urls import url
from readtube import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^Channels/$', views.ChannelPageView.as_view()),
]
