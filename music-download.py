from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import argparse
import re

def is_valid_youtube_url(url):
    # Basic YouTube URL validation
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return bool(re.match(youtube_regex, url))

def download_youtube_audio(url, output_path='.'):
    try:
        if not is_valid_youtube_url(url):
            print("Error: Invalid YouTube URL. Please provide a valid YouTube video URL.")
            return

        # Create YouTube object with error handling
        try:
            yt = YouTube(url)
        except Exception as e:
            print(f"Error accessing YouTube video: {str(e)}")
            print("This might be due to:")
            print("1. Invalid video URL")
            print("2. Video is private or age-restricted")
            print("3. Video has been removed")
            return
        
        # Get the best quality audio stream
        try:
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        except Exception as e:
            print(f"Error getting audio stream: {str(e)}")
            return
        
        if not audio_stream:
            print("No audio stream found!")
            return
        
        # Download the audio stream
        print(f"Downloading: {yt.title}")
        try:
            audio_file = audio_stream.download(output_path=output_path)
        except Exception as e:
            print(f"Error downloading audio: {str(e)}")
            return
        
        # Convert to MP3
        print("Converting to MP3...")
        try:
            audio_clip = AudioFileClip(audio_file)
            mp3_file = os.path.splitext(audio_file)[0] + '.mp3'
            audio_clip.write_audiofile(mp3_file)
            
            # Clean up the original file
            audio_clip.close()
            os.remove(audio_file)
            
            print(f"Successfully downloaded and converted to MP3: {mp3_file}")
        except Exception as e:
            print(f"Error converting to MP3: {str(e)}")
            if os.path.exists(audio_file):
                os.remove(audio_file)
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download YouTube audio as MP3')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-o', '--output', default='.', help='Output directory (default: current directory)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Download the audio
    download_youtube_audio(args.url, args.output)
