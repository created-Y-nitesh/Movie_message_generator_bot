import re

def drive_to_direct(link):
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", link)

    if not match:
        return "Invalid Google Drive Link"

    file_id = match.group(1)
    return f"https://drive.google.com/uc?export=download&id={file_id}"


# Example
# link = input("Enter Google Drive Link: ")
# print("\nDirect Download Link:")
# print(drive_to_direct(link))