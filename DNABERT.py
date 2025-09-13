import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from Bio import SeqIO 
import matplotlib.pyplot as plt
import seaborn as sns

def read_fasta_sequences(fasta_file, identifier="18S"):
    
    sequences = []
    total_records = 0
    print(f"\n1. Reading and filtering sequences from '{fasta_file}' for '{identifier}' marker...")
    try:
        for record in SeqIO.parse(fasta_file, "fasta"):
            total_records += 1
            if identifier in record.description:
                sequences.append(str(record.seq))

        print(f"   ...Found {len(sequences)} '{identifier}' sequences out of {total_records} total records.")
        return sequences
    except FileNotFoundError:
        print(f"   ...Error: The file '{fasta_file}' was not found.")
        return []

def get_dnabert_feature_matrix(sequences, model, tokenizer):
   
    if not sequences:
        print("   ...No sequences to process.")
        return None

    print("\n2. Tokenizing DNA sequences and generating embeddings...")   
    inputs = tokenizer(
        sequences,
        padding=True,
        truncation=True,
        max_length=200,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    feature_matrix_X1 = outputs.last_hidden_state
    print("   ...Feature Matrix X_1 has been successfully extracted.")
    return feature_matrix_X1

def visualize_feature_matrix(numpy_matrix, output_image_file='feature_matrix_heatmap.png'):
   
    print(f"\n4. Visualizing the feature matrix...")
    if numpy_matrix is None or numpy_matrix.shape[0] == 0:
        print("   ...Matrix is empty, skipping visualization.")
        return

    matrix_to_plot = numpy_matrix[0]

    plt.figure(figsize=(12, 4))
    sns.heatmap(matrix_to_plot, cmap='viridis')

    plt.xlabel('Embedding Dimension (0-767)')
    plt.ylabel('Token ID')
    plt.title('Heatmap of the Feature Matrix for a Single DNA Sequence')
    plt.yticks(rotation=0)

    plt.savefig(output_image_file)
    print(f"   ...Heatmap visualization saved as '{output_image_file}'")


if __name__ == "__main__":
    # --- Setup ---
    model_name = "zhihan1996/DNA_bert_6"
    print(f"Loading model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    print("...Model loaded successfully.")


    fasta_filename = "SILVA_138.2_18S_eukaryota.fasta"  
    dna_sequences_from_file = read_fasta_sequences(fasta_filename)

    feature_matrix = get_dnabert_feature_matrix(dna_sequences_from_file, model, tokenizer)

    if feature_matrix is not None:
        print("\n3. Saving the feature matrix...")
        output_filename = 'feature_matrix.npy'
        numpy_matrix = feature_matrix.cpu().numpy()
        np.save(output_filename, numpy_matrix)
        print(f"   ...Successfully saved to '{output_filename}' with shape: {numpy_matrix.shape}")

        print("\n Embedding Matrix ")
        print("Showing embeddings for the first 5 tokens of the first sequence:")
        print(numpy_matrix[0, :5, :])
        print("-" * 40)

        visualize_feature_matrix(numpy_matrix)

