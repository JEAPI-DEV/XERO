import urllib.request
import re
import subprocess
import pytube
from googleapiclient.discovery import build
import os

def get_video_id(query):
    API_KEY = "ENTER-TOKEN-HERE"
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    # Search for the song
    search_response = youtube.search().list(q=query, type='video', part='id,snippet').execute()
    
    # Select the first video
    first_video = search_response['items'][0]
    
    # Get the video URL and download the audio
    print(first_video['id']);
    print("VideoX");
    return first_video['id']['videoId']
    
def downloadYouTube(audiourl):
    """Saves a youtube video as a mp4 file at the path, in the highest quality availible"""
    yt = pytube.YouTube(audiourl)
    video = yt.streams.filter(only_audio=True).first()
    # Saves the mp3
    current_dir = os.getcwd()
    video.download(current_dir)
    return video

def play_song(query):
    vid_id = get_video_id(query + " song")
    new_query = f"https://www.youtube.com/watch?v={vid_id}"
    
    if new_query :
        filename = downloadYouTube(new_query).default_filename
    else:
        return "no audio found"
    
    print("Playing...")
    base, ext = os.path.splitext(filename)
    new_file = 'song.mp3'
    os.rename(filename, new_file)
    subprocess.Popen(['vlc', 'song.mp3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def song_query_filter(query):
    # Regex pattern to extract the search query
    query_pattern = r"play\s(?:.*\s)?(\b.+?\b)\s(?:on\s)?YouTube"
    query_match = re.search(query_pattern, query, re.IGNORECASE)

    if query_match:
        # Extract the search query
        search_query = query_match.group(1)
        return search_query
    else:
        return None
