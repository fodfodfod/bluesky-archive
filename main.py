#curl https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=densinium.bsky.social
print("AAAAAAAAAAA")
print("importing os")
import os
print("importing fetch_posts")
import fetch_posts
print("importing util")
import util
print("importing sys")
import sys
print("importing time")
import time


if __name__ == "__main__":
    #see if any users need to be added
    # os.makedirs("user_data/testing", exist_ok=True)
    print("Hello world!")
    time.sleep(1)
    try:
        with open("user_data/add_list.txt", "r") as file:
            for line in file:
                name = line.strip()
                if line.startswith("#") or not line:
                    continue
                did = util.ensure_did(name)
                if did:
                    if os.path.exists(f"user_data/{did}"):
                        print("user already added, please remove them from add_list.txt")
                    else:
                        os.makedirs(f"user_data/{did}", exist_ok=True)
                else:
                    print(f"Could not resolve DID for {name}")
    except FileNotFoundError:
        print("No add_list.txt file found")

    if len(sys.argv) == 2:
        name = sys.argv[1]
        did = util.ensure_did(name)
        if did:
            #check if the did directory exists, if not create warn the user
            if os.path.exists(f"user_data/{did}"):
                print("user already added")
            else:
                os.makedirs(f"user_data/{did}", exist_ok=True)
        else:
            print(f"Could not resolve DID for {name}")

    print("Starting to process all users...")
    #process all users
    for did in os.listdir("user_data"):
        if os.path.isdir(f"user_data/{did}"):
            try:
                print(f"Processing user: {did}")
                fetch_posts.process_user(did)
            except Exception as e:
                print(f"Error processing user {did}: {e}")