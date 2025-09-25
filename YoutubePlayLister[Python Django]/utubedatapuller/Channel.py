import os
import sys

class Channel(object):
	def __init__(self, channelId, channelTitle, playlists):
		self.id = channelId
		self.title = channelTitle
		self.playlists = playlists

	def reprJSON(self):
		return dict(id=self.id,title=self.title,playlists = self.playlists)