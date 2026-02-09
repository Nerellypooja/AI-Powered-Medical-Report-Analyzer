import easyocr
from utils.logger import get_logger

logger = get_logger(__name__)
reader = easyocr.Reader(['en'])

def extract_text(image_path):
    """
    Extracts text from image using OCR
    """
    results = reader.readtext(image_path)
    text = []
    confidence_scores = []

    for res in results:
        text.append(res[1])
        confidence_scores.append(res[2])

    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0

    return " ".join(text), avg_confidence
