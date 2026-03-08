import os
from typing import List, Optional
from ikea_recommender.app.domains.recommender.services import RecommenderService, Encoder, Reranker
from ikea_recommender.app.infrastructure.data.olist_loader import LocalOlistProductRepository
from ikea_recommender.app.infrastructure.gcp.vector_search import VertexAIVectorSearchRepository
from ikea_recommender.models.encoder import SentenceTransformerEncoder, CrossEncoderReranker
from ikea_recommender.app.core.config import settings

# Global instance for singleton pattern
_recommender_service = None

def get_recommender_service() -> RecommenderService:
    global _recommender_service
    
    if _recommender_service is None:
        print("Initializing RecommenderService (One-time setup)...")
        products_csv = os.path.join(settings.BASE_DATA_PATH, "olist_products_dataset.csv")
        translation_csv = os.path.join(settings.BASE_DATA_PATH, "product_category_name_translation.csv")
        embeddings_path = os.path.join(settings.BASE_DATA_PATH, "product_embeddings.npy")
        ids_path = os.path.join(settings.BASE_DATA_PATH, "product_ids.csv")
        
        product_repo = LocalOlistProductRepository(products_csv, translation_csv)
        vector_repo = VertexAIVectorSearchRepository(
            project_id=settings.GCP_PROJECT_ID,
            location=settings.GCP_LOCATION,
            index_id=settings.VERTEX_AI_INDEX_ID,
            embeddings_path=embeddings_path,
            ids_path=ids_path
        )
        
        encoder = SentenceTransformerEncoder()
        reranker = CrossEncoderReranker()
        
        _recommender_service = RecommenderService(
            product_repo=product_repo, 
            vector_repo=vector_repo, 
            encoder=encoder,
            reranker=reranker
        )
        
    return _recommender_service
