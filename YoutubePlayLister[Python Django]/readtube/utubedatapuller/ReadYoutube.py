from Channel import Channel
from Playlist import Playlist
from Video import Video
from Authenticator import *

from django.conf import settings

class ReadYoutube:
	def __init__(self):
		print("Program Starting")

		
	def channels_list_by_id(self, youtube):
		channels_response = youtube.channels().list(
		  mine=True,
		  part="snippet"
		).execute()

		Channels = []		
		for item in channels_response["items"]:
			Channels.append(Channel(item["id"],item["snippet"]["title"], None))
		return Channels

	def playlists_by_channel(self, youtube, channel_id):
		playlists_response = youtube.playlists().list(
			part="snippet",
				channelId = channel_id,
 		  		maxResults=50
 	 		).execute();

		Playlists = []
		for item in playlists_response["items"]:
	 		Playlists.append(Playlist(item["id"],item["snippet"]["title"], None))

		return	Playlists


	def videos_by_pl(self, youtube, pl_id):
		plvideos_response = youtube.playlistItems().list(
			part="snippet",
				playlistId = pl_id,
 		  		maxResults=50
 	 		).execute();

		Videos = []
		for item in plvideos_response["items"]:
			snippet = item["snippet"]
			if snippet is not None:
				plid = item["id"]
				title = snippet["title"]
				desc = snippet["description"]
				resourceId = snippet["resourceId"]
				
				if resourceId is not None:
					vidId = resourceId["videoId"]

				try:
					thumbnails = snippet["thumbnails"]
					
					defUrl = thumbnails["default"]["url"]
					medUrl = thumbnails["medium"]["url"]
					Videos.append(Video(vidId,title, desc, plid, defUrl, medUrl))
				except KeyError, e:
					defUrl = "/static/images/404.jpg"
					Videos.append(Video(vidId,title, desc, plid, defUrl, None))	
					pass
				except:
					pass

		return	Videos


 	def channels_with_videos(self, youtube):
		channels = self.channels_list_by_id(youtube)
		for channel in channels:
	 		playlists =  self.playlists_by_channel(youtube,channel.id)
			channel.playlists = playlists
			for pl in playlists:
				videos = self.videos_by_pl(youtube,pl.id)
				pl.videos = videos
		
		return channels		

	

