import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_latest_videos():
    # Use the Secret you stored in GitHub
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in environment.")
        return

    try:
        # Build the service (Static discovery helps avoid 'imp' module errors)
        youtube = build("youtube", "v3", developerKey=api_key, static_discovery=False)
        
        with open('channels.json', 'r') as f:
            channels = json.load(f)
        
        report = "# 📊 Fabric & Power BI Daily Update\n"
        report += f"Last updated: {os.popen('date').read()}\n\n"
        
        for name, channel_id in channels.items():
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                order="date",
                maxResults=3,
                type="video"
            )
            response = request.execute()
            
            report += f"### {name}\n"
            for item in response.get('items', []):
                title = item['snippet']['title']
                video_id = item['id']['videoId']
                url = f"https://www.youtube.com/watch?v={video_id}"
                report += f"* [{title}]({url})\n"
            report += "\n---\n"
            
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print("README.md updated successfully!")

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_latest_videos()
