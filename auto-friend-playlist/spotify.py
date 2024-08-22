import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from dotenv import load_dotenv
import os


def create_spotify_playlist(json_file_path, playlist_name=None):
    print("Starting Spotify Playlist Creator")

    # Load environment variables from .env file
    load_dotenv()

    # Spotify API credentials
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        print("Error: Spotify API credentials not found in .env file.")
        print(
            "Please ensure you have a .env file with SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI."
        )
        return

    # Set up authentication
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-private",
        )
    )

    # Load the JSON file with Spotify links
    with open(json_file_path, "r") as file:
        spotify_links = json.load(file)

    # Create a new playlist
    if not playlist_name:
        playlist_name = f"Instagram Shared Tracks {datetime.now().strftime('%Y-%m-%d')}"

    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False)

    # Add tracks to the playlist
    track_uris = []
    for item in spotify_links:
        try:
            # Extract track ID from URL
            track_id = item["url"].split("/")[-1].split("?")[0]
            track_uri = f"spotify:track:{track_id}"
            track_uris.append(track_uri)
        except Exception as e:
            print(f"Error processing track {item['title']}: {e}")

    # Spotify allows a maximum of 100 tracks per request
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist["id"], track_uris[i : i + 100])

    print(
        f"Playlist '{playlist_name}' created successfully with {len(track_uris)} tracks!"
    )
    print(f"Playlist URL: {playlist['external_urls']['spotify']}")


if __name__ == "__main__":
    json_file_path = input("Enter the path to your JSON file with Spotify links: ")
    playlist_name = input(
        "Enter a name for your playlist (or press Enter for default name): "
    )

    if not playlist_name.strip():
        playlist_name = None

    create_spotify_playlist(json_file_path, playlist_name)
