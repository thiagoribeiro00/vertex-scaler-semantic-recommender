from fastapi import APIRouter, HTTPException
from ikea_recommender.app.domains.recommender.feedback_entities import Feedback
import logging
import json

router = APIRouter(prefix="/feedback", tags=["Reinforcement Learning"])
logger = logging.getLogger("ikea_recommender.feedback")

@router.post("/log")
async def log_user_feedback(feedback: Feedback):
    """
    Captures user interaction for Reinforcement Learning (RL) reward signals.
    In production, this would be pushed to Kafka or a BigQuery buffer.
    """
    # Log as structured data for telemetry
    log_entry = {
        "event_type": "user_feedback",
        "action": feedback.action,
        "product_id": feedback.product_id,
        "user_id": feedback.user_id,
        "timestamp": feedback.timestamp.isoformat()
    }
    logger.info(json.dumps(log_entry))
    
    return {"status": "recorded", "action": feedback.action}
