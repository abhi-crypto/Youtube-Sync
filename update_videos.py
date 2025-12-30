import os
import json
import googleapiclient.discovery

def get_latest_videos():
    api_key = os.environ['YOUTUBE_API_KEY']
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    
    report = "# Latest Fabric & Power BI Videos\n\n"
    
    for name, channel_id in channels.items():
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            maxResults=3
        )
        response = request.execute()
        
        report += f"## {name}\n"
        for item in response['items']:
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            url = f"https://www.youtube.com/watch?v={video_id}"
            report += f"* [{title}]({url})\n"
        report += "\n"
        
    with open('README.md', 'w') as f:
        f.write(report)

if __name__ == "__main__":
    get_latest_videos()
