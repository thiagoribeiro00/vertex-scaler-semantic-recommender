from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Product:
    product_id: str
    product_category_name: str
    product_name_lenght: Optional[int] = None
    product_description_lenght: Optional[int] = None
    product_photos_qty: Optional[int] = None
    product_weight_g: Optional[int] = None
    product_length_cm: Optional[int] = None
    product_height_cm: Optional[int] = None
    product_width_cm: Optional[int] = None
    description: str = ""
    in_stock: bool = True

@dataclass
class Recommendation:
    product_id: str
    score: float
    product_details: Optional[Product] = None

@dataclass
class SearchResult:
    query: str
    recommendations: List[Recommendation] = field(default_factory=list)
