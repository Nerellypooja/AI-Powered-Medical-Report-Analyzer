# analysis/confidence_score.py

def get_confidence_message(confidence, threshold=0.7):
    """
    Returns a warning message if OCR confidence is below threshold.
    confidence: float between 0 and 1
    """
    if confidence < threshold:
        return (
            "⚠️ OCR confidence is low. "
            "Some values may be inaccurate. "
            "Please double-check the report or upload a clearer image."
        )
    return None
