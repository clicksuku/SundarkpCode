import os
import sys


class Playlist(object):
	def __init__(self, playlistId, title, videos):
		self.id = playlistId
		self.title = title
		self.videos = videos

	def reprJSON(self):
		return dict(id=self.id,title=self.title,videos = self.videos)