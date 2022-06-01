import os
from base64 import b64decode


def init_google_vision():
    gcp_cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

    if not os.path.exists(gcp_cred):
        bfile = b64decode(gcp_cred)
        key_path = "key.json"
        with open(key_path, "wb") as f:
            f.write(bfile)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    
