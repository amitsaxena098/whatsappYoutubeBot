from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from apiclient.discovery import build
import isodate

# Arguments that need to passed to the build function 
DEVELOPER_KEY = "AIzaSyDjXF69w5hwq1tLbJYhe-NaMhstpp14xbE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
max_results = 3

# creating Youtube Resource Object 
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

app = Flask(__name__)


@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    request_body = request.form.get('Body')
    response = MessagingResponse()
    print(request_body)
    req_body_lc = request_body.lower()
    if(req_body_lc == "help"):
        response = MessagingResponse()
        msg = response.message("*Hey fella!*\nThanks for using my bot.\nBelow are the commands that are helpful to operate this bot.\n# Send any keyword, and the bot will reply with a video that best matches the keyword.\n# Send a youtube video link and get its download link.\n#")
        return str(response)
    #num_media = int(request.values.get("NumMedia"))
    #if not num_media:
    #    msg = response.message("Send us an image!")
    #else:
    search_keyword = youtube_object.search().list(q = request_body, type = "video", part = "id, snippet", maxResults = max_results).execute()
    # extracting the results from search response 
    results = search_keyword.get("items", [])
    videos = []
    for result in results:
        if result['id']['kind'] == "youtube#video":
            videos.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], result["id"]["videoId"], result['snippet']['description'], result['snippet']['thumbnails']['high']['url']))
            response = MessagingResponse()
            vlnk = "https://www.youtubepp.com/watch?v=" + result["id"]["videoId"]
            d_search = youtube_object.videos().list(id = result["id"]["videoId"], part = "contentDetails, statistics", maxResults = max_results).execute().get("items", [])
            print(str(d_search))
            duration = isodate.parse_duration(str( (d_search[0])["contentDetails"]["duration"]))
            print(duration)
            msg = response.message("*Title:* " + result['snippet']['title'] + "\n*Duration:* " + duration + "\n*Views:* " + d_search['statistics']['viewCount'] + "\n*Channel:* " + result['snippet']['channelTitle'] + "\n\n*VideoLink:* " + "```" + "https://www.youtube.com/watch?v=" + result["id"]["videoId"] + "```" + "\n\n*Download Here:* ```" + vlnk + "```\n\n*Developed by:* ```@devilHail YO```")
            msg.media(result['snippet']['thumbnails']['high']['url'])
            return str(response)

    #msg = response.message("Link: " + down)
    #msg.media(GOOD_BOY_URL)
    #return str(response)

if __name__ == "__main__":
    app.run(debug=True)
