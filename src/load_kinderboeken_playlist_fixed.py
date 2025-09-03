#!/usr/bin/env python3
import requests
import json
import time
import sys

MOPIDY_URL = 'http://localhost:6680/mopidy/rpc'
PLAYLIST_URI = 'm3u:Kinderboeken.m3u8'

def mopidy_call(method, params=None, retries=3):
    """Send RPC call to Mopidy with retry logic"""
    if params is None:
        payload = {'method': method, 'jsonrpc': '2.0', 'id': 1}
    else:
        payload = {'method': method, 'params': params, 'jsonrpc': '2.0', 'id': 1}
    
    for attempt in range(retries):
        try:
            response = requests.post(MOPIDY_URL, 
                                   headers={'Content-Type': 'application/json'}, 
                                   data=json.dumps(payload), 
                                   timeout=5)
            result = response.json()
            if 'error' in result:
                print(f"Mopidy error: {result['error']['message']}")
                return None
            return result.get('result')
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return None

def wait_for_mopidy():
    """Wait for Mopidy to be ready"""
    print("Waiting for Mopidy to be ready...")
    max_attempts = 30  # Wait up to 60 seconds
    
    for attempt in range(max_attempts):
        try:
            state = mopidy_call('core.get_version')
            if state:
                print("Mopidy is ready!")
                return True
        except:
            pass
        
        print(f"Waiting... ({attempt + 1}/30)")
        time.sleep(2)
    
    print("Mopidy failed to start within timeout period")
    return False

def load_playlist():
    """Load the Kinderboeken playlist into tracklist"""
    print(f"Loading playlist: {PLAYLIST_URI}")
    
    # First, get the playlist contents
    playlist = mopidy_call('core.playlists.lookup', [PLAYLIST_URI])
    
    if not playlist or not playlist.get('tracks'):
        print("Failed to get playlist tracks")
        return False
    
    tracks = playlist['tracks']
    print(f"Found {len(tracks)} tracks in playlist")
    
    # Clear current tracklist
    mopidy_call('core.tracklist.clear')
    print("Cleared current tracklist")
    
    # Extract URIs from tracks
    uris = [track["uri"] for track in tracks]
    print(f"Extracted {len(uris)} URIs from tracks")
    
    # Add URIs to tracklist using correct parameter format
    result = mopidy_call('core.tracklist.add', {'uris': uris})
    if result:
        print(f"Added {len(result)} tracks to tracklist")
        
        # Get current tracklist to confirm
        tracklist = mopidy_call('core.tracklist.get_tracks')
        if tracklist:
            print(f"Tracklist now contains {len(tracklist)} tracks")
            if tracklist:
                print(f"First track: {tracklist[0].get('name', 'Unknown')}")
            return True
    
    print("Failed to load playlist")
    return False

def main():
    print("Kinderboeken Playlist Auto-Loader Starting...")
    
    if not wait_for_mopidy():
        sys.exit(1)
    
    # Add a small delay to ensure Mopidy is fully initialized
    time.sleep(3)
    
    if load_playlist():
        print("Playlist loaded successfully! Ready for button control.")
        sys.exit(0)
    else:
        print("Failed to load playlist")
        sys.exit(1)

if __name__ == '__main__':
    main()
