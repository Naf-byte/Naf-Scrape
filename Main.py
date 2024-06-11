import streamlit as st
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
import io

# Replace 'dev' with your actual API key
DEVELOPER_KEY = "AIzaSyAvLHNkmnhBsq4K2dHry56GF2EjieQYklM"

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


# Function to fetch comments for a given video
def fetch_comments(video_id):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )

        # Execute the request.
        response = request.execute()

        # Check if there are any items in the response.
        if 'items' in response and response['items']:
            # Get the comments from the response.
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append([
                    comment.get('authorDisplayName'),
                    comment.get('authorChannelId', {}).get('value', ''),
                    comment.get('authorProfileImageUrl'),
                    comment.get('publishedAt'),
                    comment.get('updatedAt'),
                    comment.get('likeCount'),
                    item['snippet'].get('totalReplyCount'),
                    comment.get('textOriginal'),
                    video_id,
                    item['snippet'].get('isPublic')
                ])

            while 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']
                nextRequest = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=nextPageToken
                )
                response = nextRequest.execute()
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append([
                        comment.get('authorDisplayName'),
                        comment.get('authorChannelId', {}).get('value', ''),
                        comment.get('authorProfileImageUrl'),
                        comment.get('publishedAt'),
                        comment.get('updatedAt'),
                        comment.get('likeCount'),
                        item['snippet'].get('totalReplyCount'),
                        comment.get('textOriginal'),
                        video_id,
                        item['snippet'].get('isPublic')
                    ])
        else:
            st.error(f"No comments found for video ID: {video_id}")

    except googleapiclient.errors.HttpError as e:
        if e.resp.status in [404, 400]:
            st.error(f"Invalid Video ID: {video_id}")
        else:
            st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    return comments


# Streamlit app
st.markdown("""
    <style>
        .centered-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #31473A;
            text-align: center;
            margin-bottom: 5px;
            text-shadow: 1px 1px 2px #ecf0f1;
        }
        .centered-subtitle {
            font-size: 1.2rem;
            color: #31473A;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 1px 1px 2px #ecf0f1;
        }
        .input-container {
            text-align: center;
        }
        .input-box {
            width: 100%;
            max-width: 500px;
            margin: auto;
        }
        .fetch-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .download-buttons-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            padding: 10px;
            margin-top: 30px;
        }
        body {
            background-color: #EDF4F2; /* White background */
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.9rem;
            color: #EDF4F2;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='centered-title'>Naf-Scrape</div>", unsafe_allow_html=True)
st.markdown("<div class='centered-subtitle'>YouTube Comments Scraper</div>", unsafe_allow_html=True)
st.markdown("<div class='centered-subtitle'>Fetch and download comments from YouTube videos in various formats</div>",
            unsafe_allow_html=True)

# Input field for video IDs
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
video_ids_input = st.text_input("Enter YouTube Video IDs (comma-separated)", "")
st.markdown("</div>", unsafe_allow_html=True)

# Button to fetch comments
if st.button("Fetch Comments"):
    if not video_ids_input.strip():
        st.warning("Please enter a YouTube Video ID first.")
    else:
        video_ids = [vid.strip() for vid in video_ids_input.split(",")]
        all_comments = []

        with st.spinner('Fetching comments...'):
            for video_id in video_ids:
                st.write(f"Fetching comments for video ID: {video_id}")
                comments = fetch_comments(video_id)
                if comments:
                    all_comments.extend(comments)

        if all_comments:
            df = pd.DataFrame(all_comments, columns=[
                'author', 'author_channel_id', 'author_profile_image',
                'published_at', 'updated_at', 'like_count', 'total_reply_count',
                'text', 'video_id', 'public'
            ])
            st.dataframe(df)

            # Save to Excel, CSV, and JSON and provide download links
            st.markdown("<div class='download-buttons-container'>", unsafe_allow_html=True)

            # Save to Excel and provide download link
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Comments')
            excel_buffer.seek(0)
            st.download_button(
                label="Download as Excel",
                data=excel_buffer,
                file_name='YouTube_Comments.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            # Save to CSV and provide download link
            csv_buffer = io.BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            st.download_button(
                label="Download as CSV",
                data=csv_buffer,
                file_name='YouTube_Comments.csv',
                mime='text/csv'
            )

            # Save to JSON and provide download link
            json_buffer = io.BytesIO()
            df.to_json(json_buffer, orient="records")
            json_buffer.seek(0)
            st.download_button(
                label="Download as JSON",
                data=json_buffer,
                file_name='YouTube_Comments.json',
                mime='application/json'
            )

            st.markdown("</div>", unsafe_allow_html=True)

#
# Footer
st.markdown("<div class='footer'>Powered by Naf-Byte (Nafay Ur Rehman)</div>", unsafe_allow_html=True)
