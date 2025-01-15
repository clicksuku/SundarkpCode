# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import dumps
import json

import sys
print (sys.path)

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

from utubedatapuller.Authenticator import get_authenticated_service
from utubedatapuller.Encoders import ComplexEncoder
from utubedatapuller.ReadYoutube import ReadYoutube
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