from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Feedback(BaseModel):
    user_id: str
    product_id: str
    action: str  # e.g., "click", "add_to_cart", "buy", "skip"
    timestamp: datetime = datetime.now()
    metadata: Optional[dict] = None

class RewardContext(BaseModel):
    session_id: str
    query: str
    reward: float  # Numerical signal for RL (e.g., click=1.0, buy=10.0)
