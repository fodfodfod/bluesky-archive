#curl https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=densinium.bsky.social
import requests
import json
import datetime
import time
import sys
import os

def load_user_data_from_file(did: str):
    # load user data from the file, note that the folder may not exist
    try:
        with open(f"user_data/{did}/posts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        pass

    # if the file does not exist, return an empty list
    return []

def request_user_data(did: str, most_recent_timestamp: datetime.datetime):
    # request user data from the API in 100 block messages, until the most recent cached post id is reached
    all_posts = []
    cursor = None
    number_of_requests = 0
    all_posts_fetched = False
    while not all_posts_fetched:
        number_of_requests += 1
        url = f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={did}&limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        data = requests.get(url).json()
        posts = data["feed"]
        for post in posts:
            # if the post is older than the most recent cached post id, return all posts
            post_timestamp = datetime.datetime.fromisoformat(post["post"]["indexedAt"])
            if most_recent_timestamp and post_timestamp <= most_recent_timestamp:
                all_posts_fetched = True
                break
            all_posts.append(post)
        cursor = data.get("cursor")
        
        if not all_posts_fetched:
            time.sleep(1)  # to avoid rate limiting
    print(f"Number of requests made: {number_of_requests}")
    return all_posts


def process_user(did: str):
    os.makedirs(f"user_data/{did}", exist_ok=True)
    # get profile
    url = f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={did}"
    profile_data = requests.get(url).json()
    handle = profile_data.get("handle", "")
    with open(f"user_data/{did}/user_data.json", "w+") as file:
        raw_file = file.read()
        if raw_file:
            user_profile_history = json.load(file)
        else:
            user_profile_history = []

        user_profile_history.insert(0, profile_data)
        json.dump(user_profile_history, file, indent=4)
    
    #get posts
    data = load_user_data_from_file(did)
    if data:
        most_recent_cached_post_timestamp = datetime.datetime.fromisoformat(data[0]["post"]["indexedAt"])
    else:
        most_recent_cached_post_timestamp = None
    new_posts = request_user_data(did, most_recent_cached_post_timestamp)
    if new_posts:
        print(f"Found {len(new_posts)} new posts for user {handle}, {did}")
        # prepend new posts to data
        data = new_posts + data
        # save data to file
        with open(f"user_data/{did}/posts.json", "w") as file:
            json.dump(data, file, indent=4)
    else:
        print(f"No new posts for user {handle}, {did}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <username or did>")
        sys.exit(1)
    name = sys.argv[1]
    #check if the username is a did, if not, convert it to a did
    if not name.startswith("did:"):
        # convert username to did
        url = f"https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={name}"
        response = requests.get(url)
        data = response.json()
        did = data["did"]

    process_user(did)