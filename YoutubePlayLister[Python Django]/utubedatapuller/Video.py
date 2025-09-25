import os
import sys

class Video(object):
	def __init__(self, videoId, title, desc, plitemId, defthumbnailURL, medthumbnailURL):
		self.id = videoId
		self.title = title
		self.desc = desc
		self.plitemId = plitemId
		self.defthumbnailURL = defthumbnailURL
		self.medthumbnailURL = medthumbnailURL
		

	def reprJSON(self):
		return dict(id=self.id,title=self.title, defthumbnailURL=self.defthumbnailURL, medthumbnailURL=self.medthumbnailURL) 