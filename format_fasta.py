import os
import tarfile
import subprocess
import glob

# --- Configuration ---
# Directory where the .tar.gz files were downloaded
DOWNLOAD_DIR = "ncbi_nt_database"
# The name of the final, combined FASTA file
OUTPUT_FASTA_FILE = "combined_nt.fasta"

try:
    print("Starting extraction and conversion process...")
    
    # --- STEP 1: Extract all downloaded archives ---
    archives = sorted(glob.glob(os.path.join(DOWNLOAD_DIR, "*.tar.gz")))
    if not archives:
        raise FileNotFoundError("No .tar.gz archives found in the directory.")
        
    db_names = []
    print(f"Found {len(archives)} archives to extract.")
    for i, archive_path in enumerate(archives):
        print(f"  - Extracting ({i+1}/{len(archives)}): {os.path.basename(archive_path)}")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=DOWNLOAD_DIR)
        
        # Store the base name of the database (e.g., "ncbi_nt_database/nt.000")
        db_base_name = archive_path.replace(".tar.gz", "")
        db_names.append(db_base_name)

    print("\n✅ Extraction complete.")

    # --- STEP 2: Convert and merge all parts into a single FASTA file ---
    print(f"\nRunning blastdbcmd to merge {len(db_names)} database parts...")
    
    # The -db argument takes a space-separated list of database names in quotes
    db_list_str = " ".join(db_names)
    output_path = os.path.join(DOWNLOAD_DIR, OUTPUT_FASTA_FILE)
    
    command = [
        "blastdbcmd",
        "-db", db_list_str,
        "-entry", "all",
        "-out", output_path,
        "-long_seqids" # Use long sequence IDs for better descriptions
    ]
    
    # Execute the command
    subprocess.run(command, check=True)
    
    print(f"\n✅ Conversion complete. Final file saved as: {output_path}")

    # --- STEP 3: Clean up intermediate files ---
    print("\nCleaning up temporary archives and extracted files...")
    
    # Get a list of all files to remove (archives and extracted binary files)
    files_to_remove = []
    for archive_path in archives:
        files_to_remove.append(archive_path)
        # Add the extracted binary files (e.g., .nhr, .nin, .nsq, etc.)
        files_to_remove.extend(glob.glob(archive_path.replace(".tar.gz", ".*")))

    for f_path in set(files_to_remove):
        if os.path.exists(f_path):
            os.remove(f_path)
            
    print("\n✅ Cleanup complete.")

# --- Error Handling ---
except FileNotFoundError:
    print("\n❌ CRITICAL ERROR: Could not find required files or directories.")
    print(f"   Ensure the '{DOWNLOAD_DIR}' directory exists and contains .tar.gz files.")
    print("   Also, ensure 'blastdbcmd' is installed and in your system's PATH.")
except subprocess.CalledProcessError as e:
    print("\n❌ CRITICAL ERROR: 'blastdbcmd' failed.")
    print("   This may be due to an issue with the BLAST+ installation or corrupted files.")