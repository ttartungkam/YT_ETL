import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
MAX_RESULTS = 50

# Get the playlist ID for the channel's uploads
def get_playlist_id():
    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        #print(json.dumps(data, indent=4))

        channel_items = data["items"][0]

        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(f'Channel Uploads Playlist ID: {channel_playlistId}\n')

        return channel_playlistId
    
    except requests.exceptions.RequestException as e:
        raise e
    
def get_video_ids(playlistId):

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}&playlistId={playlistId}&key={API_KEY}"
    video_ids = []
    pageToken = None

    try:
        while True:
            paged_url = f"{base_url}&pageToken={pageToken}" if pageToken else base_url
                
            response = requests.get(paged_url)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)  
                
            pageToken = data.get("nextPageToken")

            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e

def batch_lists(input_list, batch_size):
    for i in range(0, len(input_list), batch_size):
        yield input_list[i:i + batch_size]

def get_video_details(video_ids):
    base_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&key={API_KEY}"
    video_details = []
    pageToken = None

    try:
        while True:
            for batch in batch_lists(video_ids, 50):
                ids_string = ",".join(batch)
                url = f"{base_url}&id={ids_string}"

                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                for item in data.get("items", []):
                    video_info = {
                        "videoId": item["id"],
                        "title": item["snippet"]["title"],
                        #"description": item["snippet"]["description"],
                        "publishedAt": item["snippet"]["publishedAt"],
                        "viewCount": item["statistics"].get("viewCount", 0),
                        "likeCount": item["statistics"].get("likeCount", 0),
                        "commentCount": item["statistics"].get("commentCount", 0)
                    }
                    video_details.append(video_info)
                
                pageToken = data.get("nextPageToken")

                if not pageToken:
                    break

            return video_details

    except requests.exceptions.RequestException as e:
        raise e
    
    
if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    video_details = get_video_details(video_ids)

    print(json.dumps(video_details, indent=4))
    print(f'Total videos fetched: {len(video_details)}')