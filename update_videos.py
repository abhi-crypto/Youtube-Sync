import os
import json
from datetime import datetime
from googleapiclient.discovery import build

def get_latest_videos():
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        return

    try:
        youtube = build("youtube", "v3", developerKey=api_key, static_discovery=False)
        
        with open('channels.json', 'r') as f:
            channels = json.load(f)
        
        # Dashboard Header with Sync Date
        sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        report = f"# 📊 Fabric & Power BI Video Dashboard\n"
        report += f"> **Last Sync Date:** {sync_time}\n\n"
        report += "| Thumbnail | Channel | Video Title |\n"
        report += "| :--- | :--- | :--- |\n"
        
        for name, channel_id in channels.items():
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                order="date",
                maxResults=2, # Get top 2 latest per channel
                type="video"
            )
            response = request.execute()
            
            for item in response.get('items', []):
                title = item['snippet']['title']
                video_id = item['id']['videoId']
                thumb = item['snippet']['thumbnails']['default']['url']
                url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Adding a row to the table
                report += f"| ![{name}]({thumb}) | **{name}** | [{title}]({url}) |\n"
            
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(report)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_latest_videos()
