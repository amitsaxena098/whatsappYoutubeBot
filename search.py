from apiclient.discovery import build 

# Arguments that need to passed to the build function 
DEVELOPER_KEY = "AIzaSyDjXF69w5hwq1tLbJYhe-NaMhstpp14xbE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating Youtube Resource Object 
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY) 
print("App started")

def youtube_search_keyword(query, max_results):
	print("fun called")
	# calling the search.list method to 
	# retrieve youtube search results 
	search_keyword = youtube_object.search().list(q = query, part = "id, snippet", maxResults = max_results).execute() 
	# extracting the results from search response 
	results = search_keyword.get("items", []) 
	#print("results", results)
	# empty list to store video, 
	# channel, playlist metadata 
	videos = [] 
	playlists = [] 
	channels = [] 
	
	# extracting required info from each result object 
	for result in results: 
		# video result object 
		if result['id']['kind'] == "youtube#video": 
			videos.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], result["id"]["videoId"], result['snippet']['description'], result['snippet']['thumbnails']['high']['url'])) 
			
		# playlist result object 
		elif result['id']['kind'] == "youtube# playlist": 
			playlists.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], 
								result["id"]["playlistId"], 
								result['snippet']['description'], 
								result['snippet']['thumbnails']['default']['url'])) 

		# channel result object 
		elif result['id']['kind'] == "youtube# channel": 
			channels.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], 
								result["id"]["channelId"], 
								result['snippet']['description'], 
								result['snippet']['thumbnails']['default']['url'])) 
		
	print("Videos:\n", "\n".join(videos), "\n") 
	print("Channels:\n", "\n".join(channels), "\n") 
	print("Playlists:\n", "\n".join(playlists), "\n") 

if __name__ == "__main__":
	print("main called")
	youtube_search_keyword('jubin nautiyal', max_results = 10) 
