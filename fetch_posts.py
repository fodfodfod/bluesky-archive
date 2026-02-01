import requests
import datetime
import json
import os
import time
import logging
from util import ensure_did


def _load_user_data_from_file(did: str):
    # load user data from the file, note that the folder may not exist
    try:
        with open(f"user_data/{did}/posts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        pass

    # if the file does not exist, return an empty list
    return []

def _request_user_data(did: str, most_recent_timestamp: datetime.datetime):
    """
    Request user data from the Bluesky API, handling pagination.

    :param did: The DID of the user to fetch posts for.
    :param most_recent_timestamp: The timestamp of the most recent cached post.
    :return: A list of new posts.
    """
    logger = logging.getLogger("main")
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
        logger.debug(f"Fetched {len(posts)} posts, total so far: {len(all_posts)}, did: {did}")
        if not all_posts_fetched:
            time.sleep(1)  # to avoid rate limiting
    logger.info(f"Number of requests made: {number_of_requests}")
    return all_posts


def process_user(did: str):
    """
    Process a user by fetching their profile and posts, and saving them to files. Uses saved posts to minimize API calls.
    
    :param did: The DID of the user to process.
    """
    logger = logging.getLogger("main")
    os.makedirs(f"user_data/{did}", exist_ok=True)
    # get profile
    url = f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={did}"
    profile_data = requests.get(url).json()
    handle = profile_data.get("handle", "")
    
    # Load existing profile history if it exists
    user_profile_history = []
    user_data_file = f"user_data/{did}/user_data.json"
    if os.path.exists(user_data_file):
        try:
            with open(user_data_file, "r") as file:
                user_profile_history = json.load(file)
        except (json.JSONDecodeError, IOError):
            user_profile_history = []
    
    # Add new profile data and save
    user_profile_history.insert(0, profile_data)
    with open(user_data_file, "w") as file:
        json.dump(user_profile_history, file, indent=4)
    
    #get posts
    data = _load_user_data_from_file(did)
    if data:
        most_recent_cached_post_timestamp = datetime.datetime.fromisoformat(data[0]["post"]["indexedAt"])
    else:
        most_recent_cached_post_timestamp = None
    new_posts = _request_user_data(did, most_recent_cached_post_timestamp)
    if new_posts:
        logger.info(f"Found {len(new_posts)} new posts for user {handle}, {did}")
        # prepend new posts to data
        data = new_posts + data
        # check if there are images in the posts and add them to the download list
        for post in new_posts:
            if "embed" in post["post"]:
                embed = post["post"]["embed"]
                if "images" in embed:
                    with open(f"user_data/{did}/download_list.txt", "a") as download_file:
                        for image in embed["images"]:
                            image_url = image["fullsize"]
                            download_file.write(f"{image_url}\n")
                        
        # save data to file
        with open(f"user_data/{did}/posts.json", "w") as file:
            json.dump(data, file, indent=4)
    else:
        logger.info(f"No new posts for user {handle}, {did}")