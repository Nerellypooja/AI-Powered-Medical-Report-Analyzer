from ocr.ocr_engine import extract_text
from parser.lab_parser import parse_lab_values
from analysis.abnormal_detector import detect_abnormal

text, _ = extract_text("data/sample_reports/lab.jpeg")
labs = parse_lab_values(text)


results = detect_abnormal(labs, gender="male")

for r in results:
    print(r)
