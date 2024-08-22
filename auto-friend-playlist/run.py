import instagram
import spotify
import getpass


def run():
    print("\n" + "=" * 50)
    print("Instagram Spotify Playlist Creator")
    print("=" * 50 + "\n")

    # Instagram part
    instagram_username = input("Enter your Instagram username: ")
    instagram_password = getpass.getpass("Enter your Instagram password: ")
    friend_username = input("Enter your friend's Instagram username: ")

    json_file_path = instagram.extract_spotify_info(
        instagram_username, instagram_password, friend_username, limit=None
    )

    if json_file_path:
        # Spotify part
        playlist_name = input(
            "Enter a name for your Spotify playlist (or press Enter for default name): "
        )
        if not playlist_name.strip():
            playlist_name = None

        spotify.create_spotify_playlist(json_file_path, playlist_name)
    else:
        print("No Spotify links found. Playlist creation skipped.")


if __name__ == "__main__":
    run()
