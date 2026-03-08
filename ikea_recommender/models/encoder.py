from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List
from ..app.domains.recommender.services import Encoder

class SentenceTransformerEncoder(Encoder):
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidates: List[str]) -> List[float]:
        """
        Returns scores for each candidate relative to the query.
        """
        pairs = [[query, candidate] for candidate in candidates]
        return self.model.predict(pairs).tolist()
