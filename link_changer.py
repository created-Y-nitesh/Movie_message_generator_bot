import re

def drive_to_direct(link):
    """
    Converts a Google Drive shareable link to a direct download link.
    Returns None if the link format is not recognized.
    """
    # Pattern for /d/FILE_ID/ format (e.g. drive.google.com/file/d/FILE_ID/view)
    match_d = re.search(r"/d/([a-zA-Z0-9_-]+)", link)
    if match_d:
        file_id = match_d.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    # Pattern for id=FILE_ID format (e.g. drive.google.com/open?id=FILE_ID)
    match_id = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", link)
    if match_id:
        file_id = match_id.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    return None