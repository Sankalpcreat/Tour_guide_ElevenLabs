import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    DATA_DIR = os.path.join('app', 'data')
    SITE_INFO_PATH = os.path.join(DATA_DIR, 'site_info.json')
    EMBEDDINGS_PATH = os.path.join(DATA_DIR, 'embeddings.vec')
    METADATA_PATH = os.path.join(DATA_DIR, 'embeddings_metadata.json')

   
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    

    os.makedirs(DATA_DIR, exist_ok=True)
