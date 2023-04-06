from flask import Flask, request, render_template
import googleapiclient.discovery
import csv
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def get_video_data():
    if request.method == 'POST':
        
        video_id = request.form['video_id']

        
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

       
        with open('video_data.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Description', 'Category', 'Tags', 'View Count', 'Like Count', 'Comment Count', 'Channel Name', 'Subscriber Count'])
            writer.writerow([title, description, category, tags, view_count, like_count, comment_count, channel_name, subscriber_count])

        
        return render_template('success.html')
    
    
    return render_template('index.html')
if __name__ == '__main__':
    app.run()
