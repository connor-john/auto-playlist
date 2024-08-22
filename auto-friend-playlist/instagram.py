from instagrapi import Client
import getpass
import time
from datetime import datetime
import json


def print_section(message):
    print("\n" + "=" * 50)
    print(message)
    print("=" * 50 + "\n")


def extract_spotify_info(username, password, friend_username, limit=1000):
    print_section("Starting Instagram Spotify Link Extractor")

    def login():
        print("Logging in to Instagram...")
        client = Client()
        client.login(username, password)
        print("Login successful!")
        return client

    client = login()

    print(f"\nSearching for thread with {friend_username}...")
    threads = client.direct_threads()
    thread = next(
        (t for t in threads if friend_username in [u.username for u in t.users]), None
    )

    if not thread:
        print_section(f"No thread found with {friend_username}")
        return

    print(f"Thread found! Thread ID: {thread.id}")

    print(f"\nFetching up to {limit} messages from the thread...")
    spotify_links = {}
    total_messages = 0
    cursor = None

    while total_messages < limit:
        try:
            params = {
                "visual_message_return_type": "unseen",
                "direction": "older",
                "seq_id": "40065",
                "limit": str(min(20, limit - total_messages)),
            }
            if cursor:
                params["cursor"] = cursor

            result = client.private_request(
                f"direct_v2/threads/{thread.id}/", params=params
            )
            thread_data = result["thread"]

            messages = thread_data["items"]
            if not messages:
                break

            for message in messages:
                if message["item_type"] == "music":
                    for music_item in message["music"]:
                        target_url = music_item["target_url"]
                        if (
                            "spotify.com" in target_url
                            and target_url not in spotify_links
                        ):
                            spotify_links[target_url] = {
                                "title": music_item["title_text"],
                                "artist": music_item["caption_body_text"],
                                "url": target_url,
                            }

            total_messages += len(messages)
            print(
                f"Processing messages... (Total processed: {total_messages}, Spotify links found: {len(spotify_links)})",
                end="\r",
            )

            cursor = thread_data.get("oldest_cursor")
            if not cursor:
                break

            time.sleep(2)  # To avoid rate limiting
        except Exception as e:
            print(f"\nError fetching messages: {e}")
            if "login_required" in str(e):
                print("Session expired. Attempting to re-login...")
                client = login()
            else:
                break

    print(f"\nProcessed a total of {total_messages} messages.")
    print(f"Found {len(spotify_links)} unique Spotify links.")

    filename = f"spotify_links_{friend_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    print(f"\nSaving Spotify links to {filename}...")

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(spotify_links.values()), file, indent=2, ensure_ascii=False)

    print_section(f"Spotify links saved successfully to {filename}")


if __name__ == "__main__":
    print_section("Instagram Spotify Link Extractor")

    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")
    friend_username = input("Enter your friend's username: ")

    extract_spotify_info(username, password, friend_username)
