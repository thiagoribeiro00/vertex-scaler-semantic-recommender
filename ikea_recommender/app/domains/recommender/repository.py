from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, Recommendation

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self, limit: int = 100) -> List[Product]:
        pass

class VectorSearchRepository(ABC):
    @abstractmethod
    def search_similar(self, query_vector: List[float], top_k: int = 10) -> List[Recommendation]:
        pass

    @abstractmethod
    def get_vector_by_id(self, product_id: str) -> Optional[List[float]]:
        pass
