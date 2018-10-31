#!/usr/bin/python


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = 'AIzaSyCyT-Pa5RbyRSY1fgDWzN9mtT9LHuRYYL8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('project.html')

@app.route("/q/")
def youtube_search(query="", max_results=10):
	q = request.args.get('q')
	max_results = request.args.get('max_results')
   	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
  	search_response = youtube.search().list(q=query,part='id,snippet',maxResults=max_results).execute()
   	videos = []
   	channels = []
   	playlists = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
   	for search_result in search_response.get('items', []):
   	    if search_result['id']['kind'] == 'youtube#video':
   	        temp = dict()
   	        temp['title'] = search_result['snippet']['title']
   	        temp['publishedAt'] = search_result['snippet']['publishedAt']
   	        videos.append(temp)
   	    elif search_result['id']['kind'] == 'youtube#channel':
   	        channels.append('%s (%s)' % (search_result['snippet']['title'],search_result['id']['channelId']))
   	    elif search_result['id']['kind'] == 'youtube#playlist':
   	        playlists.append('%s (%s)' % (search_result['snippet']['title'],search_result['id']['playlistId']))
   	# return videos, channels, playlists
   	videos = sorted(videos, key=lambda k: k['title'])
   	return jsonify(videos)


if __name__ == "__main__":
    app.run(host='0.0.0.0')


# def main():
#     videos = []
#     channels = []
#     playlists = []
#     query = "surfing"#raw_input("Enter query to search : ")
#     max_results = 10 #int(raw_input("Enter no of results to get : "))
#     videos, channels, playlists = youtube_search(query, max_results)
#     print(videos)
#     videos = sorted(videos, key=lambda k: k['title'])
#     print(videos)
