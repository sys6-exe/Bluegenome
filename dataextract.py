import ftplib
import os

# --- FTP Connection Details ---
FTP_HOST = "ftp.ncbi.nlm.nih.gov"
FTP_USER = "anonymous"
FTP_PASS = ""
FTP_DB_PATH = "/blast/db/"

# --- Limit the number of files for testing ---
# --- Set to None to download all files ---
MAX_FILES_TO_DOWNLOAD = 3 

# --- Create a directory to store the downloads ---
DOWNLOAD_DIR = "ncbi_nt_database"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
    print(f" Created directory: {DOWNLOAD_DIR}")

try:
    # --- Connect and login to the FTP server ---
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.cwd(FTP_DB_PATH)
    print(" Connected and changed directory.")

    # --- Get the list of all nt archives ---
    nt_archives = [f for f in ftp.nlst() if f.startswith('nt.') and f.endswith('.tar.gz')]
    print(f"Found {len(nt_archives)} 'nt' database archives.")

    # --- Set the download limit ---
    files_to_download = nt_archives
    if MAX_FILES_TO_DOWNLOAD is not None:
        files_to_download = nt_archives[:MAX_FILES_TO_DOWNLOAD]
        print(f"Downloading the first {MAX_FILES_TO_DOWNLOAD} files...")

    # --- Loop through and download each file ---
    for i, filename in enumerate(files_to_download):
        local_filepath = os.path.join(DOWNLOAD_DIR, filename)
        print(f"Downloading file {i+1}/{len(files_to_download)}: {filename}...")
        
        with open(local_filepath, "wb") as file:
            ftp.retrbinary(f"RETR {filename}", file.write)
            
    print("\n Download complete!")
    ftp.quit()

except ftplib.all_errors as e:
    print(f" FTP error: {e}")