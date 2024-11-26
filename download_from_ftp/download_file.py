from ftplib import FTP

# FTP server credentials
ftp_server = '10.133.132.70'  # Replace with your FTP server
ftp_user = 'africa_reports'  # Replace with your username
ftp_password = 'africa_reports@123'  # Replace with your password

# Connect to the FTP server
ftp = FTP(ftp_server)
ftp.login(user=ftp_user, passwd=ftp_password)

# Specify the file to download and the local file path
remote_file_path = '/Reports/BHA_Backup/MPBN_IPRAN_Backup/2024-10-14/IPRAN/Zambia/IPRAN_ZAMBIA_Backup_2024-10-14.xlsx'  # Replace with the file's location on the server
local_file_path = './zambia_backup.xlsx'  # Local file path where you want to save the file

# Open the local file for writing in binary mode
with open(local_file_path, 'wb') as local_file:
    # Retrieve the file from the FTP server and write it to the local file
    ftp.retrbinary(f'RETR {remote_file_path}', local_file.write)

# Close the FTP connection
ftp.quit()

print(f"File downloaded and saved as {local_file_path}")
