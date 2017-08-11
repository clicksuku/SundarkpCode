# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import dumps
import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse


from utubedatapuller.ReadYoutube import *
from utubedatapuller.Encoders import ComplexEncoder

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)


class ChannelPageView(TemplateView):
    def get(self, request, **kwargs):
		youtube = get_authenticated_service()
		ry = ReadYoutube()
		channels = ry.channels_with_videos(youtube)
		js =  json.dumps([channel.reprJSON() for channel in channels], cls=ComplexEncoder)
		return render(request, 'Channels.html', {'channels_string': js})
        