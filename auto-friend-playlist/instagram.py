from instagrapi import Client
import getpass
import time
from datetime import datetime


def print_section(message):
    print("\n" + "=" * 50)
    print(message)
    print("=" * 50 + "\n")


def fetch_and_save_messages(username, password, friend_username):
    print_section("Starting Instagram Message Fetcher")

    print("Logging in to Instagram...")
    client = Client()
    client.login(username, password)
    print("Login successful!")

    print(f"\nGetting user ID for {friend_username}...")
    user_id = client.user_id_from_username(friend_username)
    print(f"User ID found: {user_id}")

    print("\nFetching direct threads...")
    threads = client.direct_threads()
    print(f"Found {len(threads)} threads")

    print(f"\nSearching for thread with {friend_username}...")
    thread = next(
        (t for t in threads if friend_username in [u.username for u in t.users]), None
    )

    if thread:
        print(f"Thread found! Thread ID: {thread.id}")

        print("\nFetching messages from the thread...")
        messages = client.direct_messages(thread.id)
        print(f"Retrieved {len(messages)} messages")

        filename = f"instagram_messages_{friend_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        print(f"\nSaving messages to {filename}...")

        with open(filename, "w", encoding="utf-8") as file:
            for i, message in enumerate(messages, 1):
                sender = client.username_from_user_id(message.user_id)
                timestamp = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                message_text = f"{timestamp} - {sender}: {message.text}\n"

                print(f"Processing message {i}/{len(messages)}", end="\r")
                file.write(message_text)

        print("\nAll messages processed and saved!")
        print_section(f"Messages saved successfully to {filename}")
    else:
        print_section(f"No thread found with {friend_username}")


if __name__ == "__main__":
    print_section("Instagram Message Fetcher")

    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")
    friend_username = input("Enter your friend's Instagram username: ")

    max_retries = 3
    for i in range(max_retries):
        try:
            fetch_and_save_messages(username, password, friend_username)
            break
        except Exception as e:
            print_section(f"An error occurred: {e}")
            if i < max_retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print_section(
                    "Max retries reached. Please check your credentials and try again later."
                )
