import pytest
from unittest.mock import MagicMock
from ikea_recommender.app.domains.recommender.entities import Product, Recommendation
from ikea_recommender.app.domains.recommender.services import RecommenderService, Encoder

def test_recommend_by_text():
    # Setup Mocks
    mock_product_repo = MagicMock()
    mock_vector_repo = MagicMock()
    mock_encoder = MagicMock()
    
    # Mock return values
    product_id = "test_product_1"
    mock_product_repo.get_by_id.return_value = Product(product_id=product_id, product_category_name="test_cat")
    mock_vector_repo.search_similar.return_value = [Recommendation(product_id=product_id, score=0.95)]
    mock_encoder.encode.return_value = [0.1] * 128
    
    # Service
    service = RecommenderService(mock_product_repo, mock_vector_repo, mock_encoder)
    
    # Run
    result = service.recommend_by_text("modern sofa", top_k=1)
    
    # Assert
    assert result.query == "modern sofa"
    assert len(result.recommendations) == 1
    assert result.recommendations[0].product_id == product_id
    assert result.recommendations[0].product_details.product_category_name == "test_cat"
    mock_encoder.encode.assert_called_once_with("modern sofa")
    mock_vector_repo.search_similar.assert_called_once()
