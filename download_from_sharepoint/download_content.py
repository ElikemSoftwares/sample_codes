from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
import os

# SharePoint site details
site_url = "https://yourdomain.sharepoint.com/sites/yoursite"
username = "your_username@yourdomain.com"
password = "your_password"
source_folder_url = "/sites/yoursite/Shared Documents/source_folder"
local_folder_path = "/path/to/your/local/folder"

# Authenticate and connect to SharePoint
ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))

# Get the source folder
source_folder = ctx.web.get_folder_by_server_relative_url(source_folder_url)
ctx.load(source_folder)
ctx.execute_query()

# Ensure the local folder exists
if not os.path.exists(local_folder_path):
    os.makedirs(local_folder_path)

# Download all files in the folder
files = source_folder.files
ctx.load(files)
ctx.execute_query()

for file in files:
    print(f"Downloading {file.name}...")
    download_path = os.path.join(local_folder_path, file.name)
    with open(download_path, "wb") as local_file:
        file.download(local_file)
        ctx.execute_query()

print("Folder downloaded successfully!")
