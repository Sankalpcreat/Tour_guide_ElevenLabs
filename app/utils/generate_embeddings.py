import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
import json
import os
import torch


device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': device}
)


with open('app/data/site_info.json', 'r', encoding='utf-8') as f:
    sites = json.load(f)

texts = []
metadata = []
for site in sites:
    site_label = site.get('siteLabel', 'Unknown site')
    latitude = site.get('latitude', 'N/A')
    longitude = site.get('longitude', 'N/A')
    description = f"{site_label} is located at coordinates {latitude}, {longitude}."
    texts.append(description)
    metadata.append({
        'id': site.get('site', '').split('/')[-1],  
        'name': site_label,
        'latitude': latitude,
        'longitude': longitude,
        'image': site.get('image', '')
    })

embeddings = model.embed_documents(texts)
embeddings_array = np.array(embeddings)

embeddings_dir='app/data'
os.makedirs(embeddings_dir,exist_ok=True)


embeddings_path=os.path.join(embeddings_dir,'embeddings.npy')
np.save(embeddings_path,embeddings_array)

metadata_path=os.path.join(embeddings_dir,'embeddings_metadata.json')
with open(metadata_path,'w',encoding='utf-8') as f:
    json.dump(metadata,f,indent=2)

if __name__ == "__main__":
    print(f"Generated embeddings shape: {embeddings_array.shape}")
    print(f"Number of sites processed: {len(metadata)}")
    print(f"Embeddings saved to: {os.path.abspath(embeddings_path)}")
    print(f"Metadata saved to: {os.path.abspath(metadata_path)}")







