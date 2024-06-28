#Naf-Scrape: YouTube Comment Scraper

Naf-Scrape is a web application built with Streamlit and the YouTube Data API v3, designed to fetch and download comments from YouTube videos in various formats. It provides a user-friendly interface where users can enter YouTube video IDs (comma-separated) and fetch comments efficiently.

Features:
Fetch Comments: Enter YouTube video IDs to retrieve comments, including author details, timestamps, likes, and replies.
Download Options: Export fetched comments into Excel, CSV, and JSON formats for further analysis and processing.
Customization: Stylish UI with themed components for a pleasant user experience.
Powered by: Built by Nafay Ur Rehman (Naf-Byte) using Streamlit.
Usage:
Input Video IDs: Enter one or more YouTube video IDs into the input field, separated by commas.
Fetch Comments: Click the "Fetch Comments" button to retrieve comments from the specified videos.
Download: Choose from Excel, CSV, or JSON download options to save the fetched data locally.
Explore Data: View comments directly in the web app interface and analyze them using the downloaded files.
Setup Instructions:
Ensure Python 3.x is installed.
Install required dependencies using pip install -r requirements.txt.
Obtain a YouTube Data API v3 key from Google Developer Console and replace DEVELOPER_KEY in app.py with your key.
Run the app using streamlit run app.py and open the provided localhost URL in your web browser.
