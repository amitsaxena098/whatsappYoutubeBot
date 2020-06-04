from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apiclient.discovery import build
from twilio.twiml.messaging_response import MessagingResponse
import pafy
import os
import json
from anonfile.anonfile import AnonFile
import time
# Arguments that need to passed to the build function 
DEVELOPER_KEY = "AIzaSyDjXF69w5hwq1tLbJYhe-NaMhstpp14xbE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
max_results = 3


# creating Youtube Resource Object 
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

# Create your views here.

@csrf_exempt
def mms_reply(request):
    request_body = request.POST.get('Body')
    search_keyword = youtube_object.search().list(q = request_body, type = "video", part = "id, snippet", maxResults = max_results).execute()
    # extracting the results from search response 
    results = search_keyword.get("items", [])
    videos = []
    if(request_body[0] != '#'):
        for result in results:
            if result['id']['kind'] == "youtube#video":
                videos.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], result["id"]["videoId"], result['snippet']['description'], result['snippet']['thumbnails']['high']['url']))
                response = MessagingResponse()
                msg = response.message("*Title:* " + result['snippet']['title'] + "\n\n*VideoLink:* " + "```" + "https://www.youtube.com/watch?v=" + result["id"]["videoId"] + "```")
                msg.media(result['snippet']['thumbnails']['high']['url'])
                return HttpResponse(str(response)) 
            else:
               response.MessagingResponse()
               msg = response.message("*SORRY....please try with different keyword.*")
               return HttpResponse(str(response))
    else:
        response = MessagingResponse()
        videoId = request_body.replace('#', '')
        if(ytmp3("https://www.youtube.com/watch?v=" + videoId) == True):
            #time.sleep(20)
            with open('./link.json') as f:
                data = json.load(f)
            mp3 = json.dumps(data['data']['file']['url']['full'])
            #mp3 = "https://anonfiles.com/V486A548ob/Pankaj_Udhas_-_Ahista_m4a"
            print("It came here " + mp3)
            #rep = "*Link to file: " + "https://google.com" + "\nPlease download file using above link"
            msg = response.message(str(mp3))
            #msg.media("https://i.giphy.com/media/PWFwdYy0da5sA/giphy.webp")
            return HttpResponse(str(response))


def ytmp3(url):
    video = pafy.new(url)
    bestaudio = video.getbestaudio(preftype ="m4a")
    bestaudio.download()
    os.system('touch link.json')
    ot = os.system('curl -F "file=@' + video.title + '.m4a" https://api.anonfiles.com/upload > link.json')
    #with open('./link.json') as f:
    #    data = json.load(f)
    #full_url = str(data['data']['file']['url']['full'])
    print(ot)
    return True
