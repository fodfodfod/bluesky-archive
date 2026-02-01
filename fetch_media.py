import time
import requests
import logging
import os

def _generate_filename_from_url(url: str) -> str:
    """
    Generate a filename from a URL by extracting the last part of the URL path.

    :param url: The URL to generate the filename from.
    :return: The generated filename.
    """
    # note that the filenames are after the last / but they use @ instead of . for the extension
    name = url.split("/")[-1]
    name = name.replace("@", ".")
    return name

def _download_image(url: str) -> int:
    """
    Download an image from a URL and save it to the appropriate user directory. This will be the user the image belongs to, regardless of who posted it.
    
    :param url: The URL of the image to download.
    :return: returns a status code or -1 on error.
    """
    logger = logging.getLogger("main")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_owner_did = url.split("/")[4]
            directory = f"user_data/{image_owner_did}/embed/"
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, _generate_filename_from_url(url)), "wb") as file:
                file.write(response.content)
            logger.info(f"Downloaded image from {url}")
            return 200
        elif response.status_code == 429:
            logger.warning(f"Rate limited when downloading image from {url}")
            return 429
        else:
            logger.error(f"Failed to download image from {url}, status code: {response.status_code}")
            return response.status_code
                
    except Exception as e:
        logger.error(f"Failed to download image from {url}: {e}")
        return -1
    
def download_user_media(did: str):
    """
    Download all media files generated from a user based on their download list.
    
    :param did: The DID of the user whose media to download.
    """
    logger = logging.getLogger("main")
    download_list_file = f"user_data/{did}/download_list.txt"
    if not os.path.exists(download_list_file):
        logger.info(f"No download list found for user {did}, skipping media download.")
        return
    
    with open(download_list_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]
    
    logger.info(f"Starting media download for user {did}, {len(urls)} files to download.")
    
    max_retries = 5
    for url in urls:
        # make sure the image isn't already downloaded
        filename = os.path.join(f"user_data/{did}/embed/", _generate_filename_from_url(url))
        if os.path.exists(filename):
            logger.warning(f"Image {filename} already exists, skipping download.")
            continue

        retries = 0
        while retries < max_retries:
            status = _download_image(url)
            if status == 200:
                # remove from download list
                with open(download_list_file, "w") as file:
                    lines = file.readlines()
                    lines = [line for line in lines if line.strip() != url]
                    file.writelines(lines)
                break
            elif status == 429:
                wait_time = 2 ** retries
                logger.warning(f"Rate limited. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                retries += 1
            else:
                logger.error(f"Failed to download {url} after {retries} retries.")
                break
        if retries == max_retries:
            logger.error(f"Exceeded maximum retries for {url}. Moving to next file.")
        
        # standard wait time
        time.sleep(1)

            

    
    logger.info(f"Completed media download for user {did}.")