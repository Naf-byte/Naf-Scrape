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
            margin-bottom: 20px;
        }
        .input-container input {
            width: 100%;
            max-width: 500px;
            margin: auto;
            border: 2px solid #31473A !important;
            border-radius: 8px !important;
            padding: 10px !important;
            background-color: #EDF4F2 !important;
            outline: none !important;
            box-shadow: none !important; /* Remove shadow on focus */
        }

        .input-container input:focus {
            border: 2px solid #31473A !important;
            box-shadow: none !important; /* Remove shadow on focus */
            outline: none !important;
        }

        .input-container input:hover {
            border: 2px solid #31473A !important;
            box-shadow: none !important; /* Remove shadow on hover */
        }

        .fetch-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .fetch-button button {
            border: 2px solid black;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 1rem;
            background-color: #FFFFFF;
            color: #31473A;
            cursor: pointer;
        }
        .download-buttons-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            padding: 10px;
            margin-top: 30px;
        }
        .download-buttons-container button {
            border: 2px solid black;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 1rem;
            background-color: #FFFFFF;
            color: #31473A;
            cursor: pointer;
        }
        body {
            background-color: #EDF4F2;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.9rem;
            color: #31473A;
        }
        .custom-table th {
            background-color: #31473A;
            color: #FFFFFF;
            text-align: center;
            padding: 10px;
        }
        .custom-table td {
            text-align: center;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='centered-title'>Naf-Scrape</div>", unsafe_allow_html=True)
st.markdown("<div class='centered-subtitle'>YouTube Comments Scraper</div>", unsafe_allow_html=True)
st.markdown("<div class='centered-subtitle'>Fetch and download comments from YouTube videos in various formats</div>",
            unsafe_allow_html=True)

# Input field for video IDs
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
video_ids_input = st.text_input("Enter YouTube Video IDs (comma-separated)", "", key="input_box", placeholder="e.g., dQw4w9WgXcQ, M7lc1UVf-VE", help="Separate multiple video IDs with commas")
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
                'Author', 'Author Channel ID', 'Author Profile Image',
                'Published At', 'Updated At', 'Like Count', 'Total Reply Count',
                'Text', 'Video ID', 'Public'
            ])
            st.dataframe(df.style.set_table_styles(
                [{
                    'selector': 'th',
                    'props': [('background-color', '#31473A'), ('color', 'white')]
                }]
            ).set_properties(**{'text-align': 'center'}))

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

# Footer
st.markdown("<div class='footer'>Powered by Naf-Byte (Nafay Ur Rehman)</div>", unsafe_allow_html=True)
