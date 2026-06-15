#!/usr/bin/env python3
"""
YouTube Playlist Downloader
Downloads playlists with quality preferences and organizes by channel/playlist
"""

import os
import subprocess
import sys
from pathlib import Path
import json
import re

class YouTubePlaylistDownloader:
    def __init__(self, base_path="/Volumes/Без названия/Edu/Youtube"):
        self.base_path = Path(base_path)
        self.quality_preferences = ["720", "480"]
        
    def ensure_base_path(self):
        """Create base directory if it doesn't exist"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def get_playlist_info(self, playlist_url):
        """Get playlist and channel information using yt-dlp"""
        try:
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--flat-playlist",
                "--no-warnings",
                playlist_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse multiple JSON objects
            lines = result.stdout.strip().split('\n')
            playlist_data = None
            
            for line in lines:
                if line.strip():
                    try:
                        data = json.loads(line)
                        if data.get('_type') == 'playlist':
                            playlist_data = data
                            break
                    except json.JSONDecodeError:
                        continue
            
            if playlist_data:
                playlist_title = playlist_data.get('title', 'Unknown Playlist')
                channel_name = playlist_data.get('uploader', 'Unknown Channel')
            else:
                # Fallback: get info without flat-playlist
                cmd_fallback = [
                    "yt-dlp",
                    "--dump-json",
                    "--playlist-items", "1",
                    "--no-warnings",
                    playlist_url
                ]
                result = subprocess.run(cmd_fallback, capture_output=True, text=True, check=True)
                lines = result.stdout.strip().split('\n')
                
                for line in lines:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            playlist_title = data.get('playlist_title', 'Unknown Playlist')
                            channel_name = data.get('uploader', data.get('channel', 'Unknown Channel'))
                            break
                        except json.JSONDecodeError:
                            continue
                else:
                    playlist_title, channel_name = 'Unknown Playlist', 'Unknown Channel'
            
            return playlist_title, channel_name
            
        except subprocess.CalledProcessError as e:
            print(f"Error getting playlist info: {e}")
            return "Unknown Playlist", "Unknown Channel"
        except Exception as e:
            print(f"Error parsing playlist info: {e}")
            return "Unknown Playlist", "Unknown Channel"
            
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
        
    def create_download_path(self, channel_name, playlist_title):
        """Create and return download path for playlist"""
        channel_path = self.base_path / self.sanitize_filename(channel_name)
        playlist_path = channel_path / self.sanitize_filename(playlist_title)
        
        channel_path.mkdir(parents=True, exist_ok=True)
        playlist_path.mkdir(parents=True, exist_ok=True)
        
        return playlist_path
        
    def download_playlist(self, playlist_url, download_path):
        """Download playlist with quality preferences"""
        # Build quality filter string correctly
        quality_filters = []
        for quality in self.quality_preferences:
            quality_filters.append(f"best[height<={quality}]")
        quality_filters.append("best")  # fallback
        
        quality_filter = "/".join(quality_filters)
        
        cmd = [
            "yt-dlp",
            "--format", quality_filter,
            "--output", str(download_path / "%(title)s.%(ext)s"),
            "--write-thumbnail",
            "--write-description", 
            "--write-info-json",
            "--embed-subs",
            "--add-metadata",
            "--merge-output-format", "mp4",
            "--no-warnings",
            playlist_url
        ]
        
        print(f"Downloading playlist to: {download_path}")
        print(f"Quality preferences: {', '.join(self.quality_preferences)}")
        print(f"Format filter: {quality_filter}")
        
        try:
            result = subprocess.run(cmd, check=True)
            print(f"Download completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e}")
            return False
            
    def process_playlist(self, playlist_url):
        """Process a single playlist"""
        print(f"\nProcessing playlist: {playlist_url}")
        
        # Get playlist information
        playlist_title, channel_name = self.get_playlist_info(playlist_url)
        print(f"Channel: {channel_name}")
        print(f"Playlist: {playlist_title}")
        
        # Create download path
        download_path = self.create_download_path(channel_name, playlist_title)
        
        # Download playlist
        success = self.download_playlist(playlist_url, download_path)
        
        if success:
            print(f"Playlist '{playlist_title}' downloaded successfully to {download_path}")
        else:
            print(f"Failed to download playlist '{playlist_title}'")
            
        return success

def main():
    # Playlists to download
    playlists = [
        "https://www.youtube.com/playlist?list=PLH-XmS0lSi_z3SEc6AWOEyQsZ0LHKaXAc",
        "https://www.youtube.com/playlist?list=PLH-XmS0lSi_z7ut6z4qsUycNXsj3cCvsk"
    ]
    
    # Check if yt-dlp is installed
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: yt-dlp is not installed or not in PATH")
        print("Please install yt-dlp: pip install yt-dlp")
        sys.exit(1)
    
    # Initialize downloader
    downloader = YouTubePlaylistDownloader()
    downloader.ensure_base_path()
    
    print("YouTube Playlist Downloader")
    print(f"Base download path: {downloader.base_path}")
    print(f"Quality preferences: {', '.join(downloader.quality_preferences)}")
    print(f"Number of playlists: {len(playlists)}")
    
    # Process each playlist
    successful_downloads = 0
    for i, playlist_url in enumerate(playlists, 1):
        print(f"\n{'='*50}")
        print(f"Playlist {i}/{len(playlists)}")
        
        if downloader.process_playlist(playlist_url):
            successful_downloads += 1
            
    print(f"\n{'='*50}")
    print(f"Download Summary:")
    print(f"Total playlists: {len(playlists)}")
    print(f"Successful: {successful_downloads}")
    print(f"Failed: {len(playlists) - successful_downloads}")
    print(f"Files saved to: {downloader.base_path}")

if __name__ == "__main__":
    main()