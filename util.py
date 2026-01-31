import requests

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
