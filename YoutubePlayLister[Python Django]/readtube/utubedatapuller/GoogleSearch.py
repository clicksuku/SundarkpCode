from google import google


class GoogleSearch(object):
	def __init__(self):
		print ("Search Module initialized")

	def SearchVideoId(videoId):
		print ("Searching for Video")
		query = "wiMMtFW5NyM	"
		num_page = 2
		search_results = google.search(query, num_page)
		print (search_results)		

	def FindAlternativeVId():
		print ("Finding Alternative Video")			