import easyocr
from utils.logger import get_logger

logger = get_logger(__name__)
reader = easyocr.Reader(['en'])

def extract_text(image_path):
    """
    Extracts text and groups it by line to preserve tabular relationships.
    """
    results = reader.readtext(image_path)
    
    # Sort results by the top-y coordinate
    results.sort(key=lambda x: x[0][0][1])

    lines = []
    if results:
        current_line_y = results[0][0][0][1]
        line_buffer = []
        
        for res in results:
            bbox, text, conf = res
            y_top = bbox[0][1]
            
            # If the word is roughly on the same vertical level (10px tolerance)
            if abs(y_top - current_line_y) < 10:
                line_buffer.append(text)
            else:
                # Close current line and start a new one
                lines.append(" ".join(line_buffer))
                line_buffer = [text]
                current_line_y = y_top
        
        # Add the last remaining line
        lines.append(" ".join(line_buffer))

    full_text = "\n".join(lines)
    avg_confidence = sum([res[2] for res in results]) / len(results) if results else 0
    
    return full_text, avg_confidence