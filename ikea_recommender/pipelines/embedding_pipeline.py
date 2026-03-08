import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from typing import List

class EmbeddingPipeline:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.base_path = "data/"

    def run(self):
        """
        1. Load Olist products.
        2. Generate item descriptions (category + metadata).
        3. Generate embeddings.
        4. Save/Upload to Vertex AI Search.
        """
        products_path = os.path.join(self.base_path, "olist_products_dataset.csv")
        translation_path = os.path.join(self.base_path, "product_category_name_translation.csv")
        
        df = pd.read_csv(products_path)
        translation = pd.read_csv(translation_path)
        
        df = df.merge(translation, on='product_category_name', how='left')
        df['product_category_name_english'] = df['product_category_name_english'].fillna('unknown')
        
        # Create a cleaner descriptive text for each product
        def generate_description(row):
            cat = row['product_category_name_english']
            dims = []
            if not pd.isna(row['product_length_cm']): dims.append(f"{int(row['product_length_cm'])}cm length")
            if not pd.isna(row['product_height_cm']): dims.append(f"{int(row['product_height_cm'])}cm height")
            if not pd.isna(row['product_width_cm']): dims.append(f"{int(row['product_width_cm'])}cm width")
            dim_str = ", ".join(dims) if dims else "dimensions unknown"
            return f"A product in the {cat} category. {dim_str}."

        df['item_description'] = df.apply(generate_description, axis=1)
        
        print(f"Generating embeddings for {len(df)} products...")
        embeddings = self.model.encode(df['item_description'].tolist(), show_progress_bar=True)
        
        # Save embeddings locally for this demo (In production, upload to GCS/Vertex AI)
        output_path = os.path.join(self.base_path, "product_embeddings.npy")
        np.save(output_path, embeddings)
        
        # Save corresponding IDs
        ids_path = os.path.join(self.base_path, "product_ids.csv")
        df[['product_id']].to_csv(ids_path, index=False)
        
        print(f"Embeddings saved to {output_path}")
        print(f"Product IDs saved to {ids_path}")
        
        # Here you would call Vertex AI Search indexing logic
        # Example: upload_to_gcs(output_path) -> update_matching_engine_index()

if __name__ == "__main__":
    pipeline = EmbeddingPipeline()
    pipeline.run()
