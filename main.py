#curl https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=densinium.bsky.social
import logging
import os
import fetch_media
import fetch_posts
import util
import sys
import time




def main():
    #see if any users need to be added
    # os.makedirs("user_data/testing", exist_ok=True)

    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)
    #set log string
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    for handler in logger.handlers:
        handler.setFormatter(logger_formatter)
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(logging.FileHandler("logs/main.log"))

    logger.info("Starting bluesky archive process")

    try:
        with open("user_data/add_list.txt", "r") as file:
            for line in file:
                name = line.strip()
                if line.startswith("#") or not line:
                    continue
                did = util.ensure_did(name)
                if did:
                    if os.path.exists(f"user_data/{did}"):
                        logger.warning(f"User {name} already added, please remove them from add_list.txt")
                    else:
                        os.makedirs(f"user_data/{did}", exist_ok=True)
                        logger.info(f"Added user {name} with DID {did}")
                else:
                    logger.error(f"Could not resolve DID for {name}")
    except FileNotFoundError:
        logger.info("No add_list.txt file found, skipping file-based user addition step")

    if len(sys.argv) == 2:
        name = sys.argv[1]
        did = util.ensure_did(name)
        if did:
            #check if the did directory exists, if not create warn the user
            if os.path.exists(f"user_data/{did}"):
                logger.warning(f"User {name} already added")
            else:
                os.makedirs(f"user_data/{did}", exist_ok=True)
                logger.info(f"Added user {name} with DID {did}")
        else:
            logger.error(f"Could not resolve DID for {name}")

    logger.info("Starting to process all users...")
    #process all users
    for did in os.listdir("user_data"):
        if os.path.isdir(f"user_data/{did}"):
            try:
                logger.debug(f"Processing user: {did}")
                fetch_posts.process_user(did)
            except Exception as e:
                logger.error(f"Error processing user {did}: {e}")
    
    logger.info("Users post fetching complete.")
    logger.info("Fetching media files...")

    for did in os.listdir("user_data"):
        if os.path.isdir(f"user_data/{did}"):
            try:
                fetch_media.download_user_media(did)
            except Exception as e:
                logger.error(f"Error downloading media for user {did}: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}\nScript terminating.")
        sys.exit(1)