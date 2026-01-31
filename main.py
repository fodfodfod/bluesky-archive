#curl https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=densinium.bsky.social
import os
from fetch_posts import process_user
from util import ensure_did
import sys


if __name__ == "__main__":
    #see if any users need to be added
    try:
        with open("user_data/add_list.txt", "r") as file:
            for line in file:
                name = line.strip()
                if line.startswith("#") or not line:
                    continue
                did = ensure_did(name)
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
        did = ensure_did(name)
        if did:
            #check if the did directory exists, if not create warn the user
            if os.path.exists(f"user_data/{did}"):
                print("user already added")
            else:
                os.makedirs(f"user_data/{did}", exist_ok=True)
        else:
            print(f"Could not resolve DID for {name}")


    #process all users
    for did in os.listdir("user_data"):
        if os.path.isdir(f"user_data/{did}"):
            try:
                print(f"Processing user: {did}")
                process_user(did)
            except Exception as e:
                print(f"Error processing user {did}: {e}")