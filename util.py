import requests
import json
import logging

def ensure_did(name: str) -> str:
    """
    Ensure the provided name is a DID. If it's a username, convert it to a DID.
    
    :param name: Handle or DID of the user
    :return: DID for the user, or None if conversion fails
    """
    if not name.startswith("did:"):
        # convert username to did
        url = f"https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={name}"
        try:
            response = requests.get(url)
            data = response.json()
            did = data["did"]
            return did
        except Exception as e:
            print(f"Error resolving handle to DID: {e}")
            return None
    return name

def did_to_username(did: str, local_only: bool = True) -> str:
    """
    Convert a DID to a username. If local_only is True, do not query the API and only use cached data.
    NOTE: This function is not guaranteed to return a username since it relies on cached data. It should be used for logging and display purposes only, not for critical functionality.
    
    :param did: The DID to convert
    :param local_only: Whether to only use cached data or fetch from the API
    :return: The username or an empty string if conversion fails
    """
    logger = logging.getLogger("main")
    try:
        with open(f"user_data/{did}/user_data.json", "r") as file:
            data = json.load(file)[0] # everytime profile data is pulled the new data is put at index 0
            handle = data["handle"]
            return handle
    except:
        if local_only:
            return ""
        # fetch from API
        url = f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={did}"
        try:
            response = requests.get(url)
            data = response.json()
            handle = data.get("handle", "")
            return handle
        except Exception as e:
            logger.error(f"Error converting DID to username. DID: {did}, Error: {e}")
            return ""