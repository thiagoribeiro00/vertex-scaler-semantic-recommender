import pandas as pd
from typing import List, Optional, Dict
from ikea_recommender.app.domains.recommender.entities import Product
from ikea_recommender.app.domains.recommender.repository import ProductRepository

class LocalOlistProductRepository(ProductRepository):
    def __init__(self, products_csv_path: str, category_translation_path: str):
        self.products_df = pd.read_csv(products_csv_path)
        self.category_translation = pd.read_csv(category_translation_path)
        
        # Merge to get English names
        self.products_df = self.products_df.merge(
            self.category_translation, 
            on='product_category_name', 
            how='left'
        )
        
        # Rename and fillna
        self.products_df['product_category_name_english'] = self.products_df['product_category_name_english'].fillna('unknown')
        self.products_map: Dict[str, Product] = {}
        self._load_products()

    def _load_products(self):
        for _, row in self.products_df.iterrows():
            # Handle NaNs
            def clean_val(val):
                return int(val) if not pd.isna(val) else None

            product = Product(
                product_id=row['product_id'],
                product_category_name=row['product_category_name_english'],
                product_name_lenght=clean_val(row['product_name_lenght']),
                product_description_lenght=clean_val(row['product_description_lenght']),
                product_photos_qty=clean_val(row['product_photos_qty']),
                product_weight_g=clean_val(row['product_weight_g']),
                product_length_cm=clean_val(row['product_length_cm']),
                product_height_cm=clean_val(row['product_height_cm']),
                product_width_cm=clean_val(row['product_width_cm'])
            )
            
            # Better description for semantinc search
            dims = []
            if product.product_length_cm: dims.append(f"{product.product_length_cm}cm length")
            if product.product_height_cm: dims.append(f"{product.product_height_cm}cm height")
            if product.product_width_cm: dims.append(f"{product.product_width_cm}cm width")
            dim_str = ", ".join(dims) if dims else "dimensions unknown"
            
            product.description = f"A product in the {product.product_category_name} category. {dim_str}."
            self.products_map[product.product_id] = product

    def get_by_id(self, product_id: str) -> Optional[Product]:
        return self.products_map.get(product_id)

    def get_all(self, limit: int = 100) -> List[Product]:
        return list(self.products_map.values())[:limit]
