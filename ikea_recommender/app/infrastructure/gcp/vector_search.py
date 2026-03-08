from typing import List, Optional
import os
import pandas as pd
import numpy as np
from ikea_recommender.app.domains.recommender.entities import Recommendation
from ikea_recommender.app.domains.recommender.repository import VectorSearchRepository

class VertexAIVectorSearchRepository(VectorSearchRepository):
    """
    Implementation of VectorSearchRepository using Google Cloud Vertex AI Search.
    Note: In a real production environment, this would use the google-cloud-aiplatform library.
    For this implementation, we simulate the behavior for demonstration.
    """
    def __init__(self, project_id: str, location: str, index_id: str, embeddings_path: Optional[str] = None, ids_path: Optional[str] = None):
        self.project_id = project_id
        self.location = location
        self.index_id = index_id
        
        # Local search data
        self._embeddings = None
        self._product_ids = None
        
        if embeddings_path and os.path.exists(embeddings_path) and ids_path and os.path.exists(ids_path):
            print(f"Loading local embeddings from {embeddings_path}...")
            self._embeddings = np.load(embeddings_path)
            self._product_ids = pd.read_csv(ids_path)['product_id'].tolist()

    def search_similar(self, query_vector: List[float], top_k: int = 10) -> List[Recommendation]:
        """
        Simulates Vertex AI ANN search or performs local KNN if data is loaded.
        """
        if self._embeddings is not None:
            # Local KNN search using Cosine Similarity
            query_vec = np.array(query_vector)
            
            # Normalization for cosine similarity
            norm_query = np.linalg.norm(query_vec)
            norm_embeddings = np.linalg.norm(self._embeddings, axis=1)
            
            # Avoid division by zero
            dot_product = np.dot(self._embeddings, query_vec)
            similarities = dot_product / (norm_embeddings * norm_query + 1e-9)
            
            # Get top K indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            recommendations = []
            for idx in top_indices:
                recommendations.append(Recommendation(
                    product_id=self._product_ids[idx],
                    score=float(similarities[idx])
                ))
            return recommendations

        # In production (GCP):
        # aiplatform.init(project=self.project_id, location=self.location)
        # index_endpoint = aiplatform.MatchingEngineIndexEndpoint(self.index_id)
        # results = index_endpoint.find_neighbors(queries=[query_vector], num_neighbors=top_k)
        
        return []

    def get_vector_by_id(self, product_id: str) -> Optional[List[float]]:
        if self._product_ids and product_id in self._product_ids:
            idx = self._product_ids.index(product_id)
            return self._embeddings[idx].tolist()
        return None

    def upsert_vector(self, product_id: str, vector: List[float]):
        pass # In local mode we use the static .npy file
