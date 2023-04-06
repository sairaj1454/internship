import csv
import googleapiclient.discovery
import os
import urllib.request
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_video_data():
    if request.method == 'POST':
        # Get the video ID from the form data
        video_id = request.form['video_id']

        # Use the code provided to get the video data
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBt935UrBealXgjpqw2F89vHFw1DdZ9bSs")
        video = youtube.videos().list(part="snippet,statistics", id=video_id).execute()["items"][0]
        title = video["snippet"]["title"]
        description = video["snippet"]["description"]
        category = video["snippet"]["categoryId"]
        tags = ",".join(video["snippet"]["tags"])
        view_count = video["statistics"]["viewCount"]
        like_count = video["statistics"]["likeCount"]
        comment_count = video["statistics"]["commentCount"]
        channel_id = video["snippet"]["channelId"]
        channel_name = youtube.channels().list(part="snippet", id=channel_id).execute()["items"][0]["snippet"]["title"]
        subscriber_count = youtube.channels().list(part="statistics", id=channel_id).execute()["items"][0]["statistics"]["subscriberCount"]

        # Download the video to the server
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_filename = f'{video_id}.mp4'
        urllib.request.urlretrieve(video_url, video_filename)

        # Write the video data to a CSV file
        with open('video_data.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Description', 'Category', 'Tags', 'View Count', 'Like Count', 'Comment Count', 'Channel Name', 'Subscriber Count', 'Video Filename'])
            writer.writerow([title, description, category, tags, view_count, like_count, comment_count, channel_name, subscriber_count, video_filename])

        # Render a success message to the user
        return render_template('success.html')
    
    # Render the form to the user
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('', filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
video_url = f'https://www.youtube.com/watch?v={video_id}'
video_filename = f'{video_id}.mp4'
urllib.request.urlretrieve(video_url, video_filename)
