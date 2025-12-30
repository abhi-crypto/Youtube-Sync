import os
import json
from datetime import datetime
from googleapiclient.discovery import build

def get_latest_videos():
    api_key = os.environ.get('YOUTUBE_API_KEY')
    youtube = build("youtube", "v3", developerKey=api_key, static_discovery=False)
    
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    
    sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    report = f"# 📊 Fabric & Power BI Video Dashboard\n"
    report += f"> **Last Sync Date:** {sync_time}\n\n"
    report += "| Thumbnail | Channel | Video Title |\n"
    report += "| :--- | :--- | :--- |\n"
    
    found_any = False # Track if we find anything at all

    for name, channel_id in channels.items():
        print(f"Searching for: {name} ({channel_id})")
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id.strip(), # strip() removes accidental spaces
            order="date",
            maxResults=3,
            type="video" 
        )
        response = request.execute()
        items = response.get('items', [])
        print(f"Found {len(items)} videos for {name}")

        for item in items:
            found_any = True
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            thumb = item['snippet']['thumbnails']['default']['url']
            url = f"https://www.youtube.com/watch?v={video_id}"
            report += f"| ![{name}]({thumb}) | **{name}** | [{title}]({url}) |\n"
            
    if not found_any:
        report += "\n**DEBUG: No videos were found. Check your Channel IDs or API permissions.**\n"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    get_latest_videos()
