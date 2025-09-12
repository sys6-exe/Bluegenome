import os
from Bio import SeqIO

FASTA_FILE = os.path.join("ncbi_nt_database", "18S_sequences.fasta")
RECORDS_TO_VIEW = 5

print(f"Displaying annotations and sequences for the first {RECORDS_TO_VIEW} records...")

try:
    with open(FASTA_FILE, "r") as handle:
        for i, record in enumerate(SeqIO.parse(handle, "fasta")):
            print("-" * 50)
            
            # Print the annotation header
            print(f"Annotation: {record.description}")
            
            # Print the first 60 characters of the DNA sequence
            print(f"Sequence:   {record.seq[:60]}...")
            
            if i + 1 >= RECORDS_TO_VIEW:
                break

except FileNotFoundError:
    print(f" ERROR: The file was not found. Please check the path.")