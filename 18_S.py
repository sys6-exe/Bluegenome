import os
from Bio import SeqIO


SOURCE_FASTA = os.path.join("ncbi_nt_database", "combined_nt.fasta")


OUTPUT_FASTA = os.path.join("ncbi_nt_database", "18S_sequences.fasta")

# Keywords to identify 18S rRNA gene sequences
MARKER_GENE_KEYWORDS = [
    "18S ribosomal RNA",
    "18S rRNA",
    "SSU rRNA",
    "small subunit ribosomal RNA"
]

found_count = 0
print(f"🔬 Starting to extract 18S sequences from '{SOURCE_FASTA}'...")
print(f"   This may take a while depending on the file size.")

try:
    # 'w' mode opens the file for writing (creates it if it doesn't exist)
    with open(SOURCE_FASTA, "r") as handle_in, open(OUTPUT_FASTA, "w") as handle_out:
        # Loop through each record in the big source file
        for record in SeqIO.parse(handle_in, "fasta"):
            # Check if the record description contains any of our 18S keywords
            if any(keyword in record.description for keyword in MARKER_GENE_KEYWORDS):
                # If it's a match, write the entire record to our new file
                SeqIO.write(record, handle_out, "fasta")
                found_count += 1

    print(f"\n Process complete.")
    print(f"   Found and saved {found_count:,} sequences to '{OUTPUT_FASTA}'.")

except FileNotFoundError:
    print(f" ERROR: The source file was not found at '{SOURCE_FASTA}'. Please check the path.")
except Exception as e:
    print(f"An error occurred: {e}")