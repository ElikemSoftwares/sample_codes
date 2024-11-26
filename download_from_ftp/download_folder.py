import os
import zipfile
from ftplib import FTP
import shutil

# FTP server credentials
ftp_server = '10.133.132.70'  # Replace with your FTP server
ftp_user = 'africa_reports'  # Replace with your username
ftp_password = 'africa_reports@123'  # Replace with your password

# Directory on the FTP server to download
ftp_folder = '/Reports/BHA_Backup/MPBN_IPRAN_Backup/2024-10-14/IPRAN/Zambia'  # Replace with your target folder on the server
local_folder = './zambia'  # Local folder to store downloaded files
zip_file_name = 'zambia_backup.zip'  # Name of the resulting zip file

# Connect to the FTP server
ftp = FTP(ftp_server)
ftp.login(user=ftp_user, passwd=ftp_password)

# Ensure the local folder exists
if not os.path.exists(local_folder):
    os.makedirs(local_folder)

def download_ftp_tree(ftp, remote_dir, local_dir):
    """
    Recursively download the contents of an FTP directory, including subdirectories.
    """
    # Make local directory if it doesn't exist
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Change to the remote directory
    ftp.cwd(remote_dir)

    # List directory contents
    file_list = ftp.nlst()

    for item in file_list:
        local_path = os.path.join(local_dir, item)
        remote_path = os.path.join(remote_dir, item)

        try:
            # Try to change directory (if successful, it's a directory)
            ftp.cwd(item)
            print(f"Entering directory: {item}")

            # Recursively download the directory
            download_ftp_tree(ftp, remote_path, local_path)

            # Go back to the parent directory after processing
            ftp.cwd('..')
        except Exception as e:
            # If changing directory fails, it's a file, so download it
            print(f"Downloading file: {item}")
            with open(local_path, 'wb') as local_file:
                ftp.retrbinary(f'RETR {item}', local_file.write)

# Start recursive download from the root folder
download_ftp_tree(ftp, ftp_folder, local_folder)
print("Folder copy completed successfully")

# Zip the folder
# shutil.make_archive(local_folder, 'zip', local_folder)
# print(f"Folder zipped as {zip_file_name}")

# Close the FTP connection
ftp.quit()

# Optionally clean up the local folder after zipping
# shutil.rmtree(local_folder)
# print(f"Local folder '{local_folder}' removed after zipping.")
