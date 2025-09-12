import torch
import numpy as np 
from transformers import AutoTokenizer, AutoModel

model_name = "zhihan1996/DNA_bert_6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

sample_dna_sequences = [
    "ATGC",
    "GATTACA"
]

inputs = tokenizer(sample_dna_sequences, padding=True, truncation=True, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
feature_matrix = outputs.last_hidden_state

print("--- Exporting the Feature Matrix ---")

numpy_matrix = feature_matrix.cpu().numpy()

np.save('feature_matrix.npy', numpy_matrix)

print(f"Feature matrix successfully saved to 'feature_matrix.npy'")
print(f"Shape of the saved matrix: {numpy_matrix.shape}")