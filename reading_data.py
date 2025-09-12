import os
from Bio import SeqIO

# --- Configuration ---
FASTA_FILE = os.path.join("ncbi_nt_database", "combined_nt.fasta")
RECORDS_TO_PROCESS = 10000000

# --- Analysis Variables ---
total_sequences = 0
eukaryotic_sequences = 0
eighteenS_sequences = 0


EUKARYOTIC_KEYWORDS = [
    "Eukaryota",    # The domain itself
    "Metazoa",      # The animal kingdom
    "Chordata",     # The phylum for vertebrates (catches Panda, Whale, etc.)
    "Fungi",        # The fungus kingdom
    "Viridiplantae" # The plant kingdom
]
MARKER_GENE_KEYWORDS = [
    "18S ribosomal RNA",
    "18S rRNA",
    "SSU rRNA",
    "small subunit ribosomal RNA"
]

print(f"🔬 Starting analysis of '{FASTA_FILE}' with a smarter filter...")

try:
    with open(FASTA_FILE, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            total_sequences += 1

            # Print the description for the first 10 records for review
            if total_sequences <= 10:
                print(f"  - Record {total_sequences}: {record.description}")

            # Check if ANY of the keywords in our list are in the description
            if any(keyword in record.description for keyword in MARKER_GENE_KEYWORDS):
                eighteenS_sequences += 1
    # This is likely an 18S rRNA sequence
    # Save it to a new file, analyze it, etc.
            if any(keyword in record.description for keyword in EUKARYOTIC_KEYWORDS):
                eukaryotic_sequences += 1
 

            if RECORDS_TO_PROCESS is not None and total_sequences >= RECORDS_TO_PROCESS:
                break
    
    print("\n Analysis complete.")
    if RECORDS_TO_PROCESS is not None:
        print(f"   (Processed the first {total_sequences:,} sequences)")
    
    print(f"\n--- Results ---")
    print(f"Total Sequences Analyzed: {total_sequences:,}")
    print(f"18S rRNA Sequences Found: {eighteenS_sequences:,}")
    print(f"Eukaryotic Sequences Found: {eukaryotic_sequences:,}")

except FileNotFoundError:
    print(f"ERROR: The file was not found at '{FASTA_FILE}'. Please check the path.")
except Exception as e:
    print(f"An error occurred during analysis: {e}")