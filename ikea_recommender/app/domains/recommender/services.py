from typing import List, Optional
from ikea_recommender.app.domains.recommender.entities import Product, Recommendation, SearchResult
from ikea_recommender.app.domains.recommender.repository import ProductRepository, VectorSearchRepository
from abc import ABC, abstractmethod

class Encoder(ABC):
    @abstractmethod
    def encode(self, text: str) -> List[float]:
        pass

class Reranker(ABC):
    @abstractmethod
    def rerank(self, query: str, candidates: List[str]) -> List[float]:
        pass

class RecommenderService:
    def __init__(
        self, 
        product_repo: ProductRepository, 
        vector_repo: VectorSearchRepository,
        encoder: Encoder,
        reranker: Optional[Reranker] = None,
        cache=None
    ):
        self._product_repo = product_repo
        self._vector_repo = vector_repo
        self._encoder = encoder
        self._reranker = reranker
        self._cache = cache

    def recommend_by_text(self, query: str, top_k: int = 10) -> SearchResult:
        """
        Main logic for semantic recommendation.
        1. Convert text to vector.
        2. Search similar vectors in Vertex AI.
        3. Rerank results for higher accuracy.
        4. Enrich with product details from DB.
        """
        # 1. Encode
        query_vector = self._encoder.encode(query)
        
        # 2. Search (Vector Search) - fetch more if reranking
        search_top_k = top_k * 5 if self._reranker else top_k
        recommendations = self._vector_repo.search_similar(query_vector, top_k=search_top_k)
        
        # 3. Enrich with DB & Apply Business Rules
        enriched_recs = []
        for rec in recommendations:
            product = self._product_repo.get_by_id(rec.product_id)
            if product and product.in_stock: # Business Rule: Only in stock
                rec.product_details = product
                enriched_recs.append(rec)
        
        # 4. Optional: Rerank for superior accuracy
        if self._reranker and enriched_recs:
            descriptions = [r.product_details.description for r in enriched_recs]
            rerank_scores = self._reranker.rerank(query, descriptions)
            for i, score in enumerate(rerank_scores):
                enriched_recs[i].score = score
            
            # Sort by rerank scores
            enriched_recs.sort(key=lambda x: x.score, reverse=True)
        
        return SearchResult(query=query, recommendations=enriched_recs[:top_k])

    def recommend_by_id(self, product_id: str, top_k: int = 10) -> SearchResult:
        """
        Recommend based on an existing product.
        """
        # Get product vector from storage
        vector = self._vector_repo.get_vector_by_id(product_id)
        if not vector:
            # Fallback: get product data and encode it
            product = self._product_repo.get_by_id(product_id)
            if not product:
                return SearchResult(query=f"Product {product_id} not found")
            vector = self._encoder.encode(product.description)
            
        recommendations = self._vector_repo.search_similar(vector, top_k=top_k)
        
        # Filter out the source product if it appeared in results
        recommendations = [r for r in recommendations if r.product_id != product_id]
        
        # Enrich
        for rec in recommendations:
            product = self._product_repo.get_by_id(rec.product_id)
            if product:
                rec.product_details = product
                
        return SearchResult(query=f"Recommendations for {product_id}", recommendations=recommendations[:top_k])
