from googlesearch import search

class GoogleSearch(object):
	def __init__(self):
		print ("Search Module initialized")

	def SearchVideoId(videoId):
		print ("Searching for Video")
		query = "wiMMtFW5NyM	"
		num_page = 2
		search_results = search.search(query, num_page)
		print (search_results)		

	def FindAlternativeVId():
		print ("Finding Alternative Video")			