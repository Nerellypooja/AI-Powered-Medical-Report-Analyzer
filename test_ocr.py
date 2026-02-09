from ocr.ocr_engine import extract_text

text, confidence = extract_text("data/sample_reports/lab.jpeg")

print("OCR TEXT:\n", text)
print("CONFIDENCE:", confidence)
