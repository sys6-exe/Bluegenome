import os
from Bio import SeqIO
import itertools
import csv

FASTA_FILE = os.path.join("ncbi_nt_database", "18S_sequences.fasta")
# The output file for our numerical fingerprints
CSV_OUTPUT_FILE = os.path.join("ncbi_nt_database", "4mer_fingerprints.csv")
# The value of k for our k-mers
K = 4

# --- Main Script ---
print(f"Starting k-mer conversion for k={K}...")
print(f"Input file: {FASTA_FILE}")

try:
    # 1. Generate all possible k-mers to use as our feature columns
    bases = ['A', 'T', 'C', 'G']
    # This creates a list of all 256 possible 4-mers ('AAAA', 'AAAC', etc.)
    all_possible_kmers = [''.join(p) for p in itertools.product(bases, repeat=K)]
    
    # Create a dictionary to hold k-mer counts, initialized to zero
    kmer_template_dict = {kmer: 0 for kmer in all_possible_kmers}

    # 2. Open the CSV file to write the output
    with open(CSV_OUTPUT_FILE, 'w', newline='') as csvfile:
        # Define the header row for the CSV file
        header = ['sequence_id'] + all_possible_kmers
        writer = csv.writer(csvfile)
        writer.writerow(header)

        # 3. Read the FASTA file and process each sequence
        record_count = 0
        with open(FASTA_FILE, "r") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                record_count += 1

                # Copy the template dictionary for this sequence's counts
                sequence_kmer_counts = kmer_template_dict.copy()

                # --- Count k-mers for the current sequence ---
                sequence_str = str(record.seq).upper()
                for i in range(len(sequence_str) - K + 1):
                    kmer = sequence_str[i:i+K]
                    # Only count valid k-mers (no 'N' or other ambiguous bases)
                    if kmer in sequence_kmer_counts:
                        sequence_kmer_counts[kmer] += 1
                
                # --- Prepare the row to write to the CSV ---
                # The row starts with the sequence ID
                row = [record.id]
                # Append the counts for each k-mer in the correct order
                for kmer in all_possible_kmers:
                    row.append(sequence_kmer_counts[kmer])
                
                # Write the row to the file
                writer.writerow(row)
                
                # Print a progress update every 10,000 records
                if record_count % 10000 == 0:
                    print(f"   ...processed {record_count:,} sequences")

    print(f"\n Conversion complete.")
    print(f"   Processed a total of {record_count:,} sequences.")
    print(f"   Numerical fingerprints saved to: '{CSV_OUTPUT_FILE}'")

except FileNotFoundError:
    print(f" ERROR: The input file was not found at '{FASTA_FILE}'. Please check that the file exists.")
except Exception as e:
    print(f"An error occurred: {e}")