from ocr.ocr_engine import extract_text
from parser.lab_parser import parse_lab_values

text, conf = extract_text("data/sample_reports/lab.jpeg")

labs = parse_lab_values(text)

for lab in labs:
    print(lab)
