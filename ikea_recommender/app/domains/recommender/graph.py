from typing import List, Dict

class KnowledgeGraphService:
    """
    Simulates a Knowledge Graph layer for Hybrid Recommendation.
    Connects categories and items semantically (e.g., cross-selling).
    """
    def __init__(self):
        # Simplified adjacency list for category relationships
        self._category_graph = {
            "office_furniture": ["stationery", "computers"],
            "baby": ["toys", "fashion_childrens_clothes"],
            "bed_bath_table": ["housewares", "cool_stuff"],
            "housewares": ["home_construction", "garden_tools"]
        }

    def get_related_categories(self, category: str) -> List[str]:
        return self._category_graph.get(category, [])

    def enrich_recommendations_with_graph(self, category: str, limit: int = 3) -> List[str]:
        """
        Suggests categories to explore based on the current context.
        """
        return self.get_related_categories(category)[:limit]
