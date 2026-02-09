import re

# Known lab tests we want to extract
KNOWN_TESTS = [
    "HEMOGLOBIN",
    "TOTAL LEUKOCYTE COUNT",
    "NEUTROPHILS",
    "LYMPHOCYTE",
    "EOSINOPHILS",
    "MONOCYTES",
    "BASOPHILS",
    "PLATELET COUNT",
    "HEMATOCRIT",
    "MCV",
    "MCH",
    "MCHC"
]

def parse_lab_values(text):
    """
    Extract lab test values from OCR text in a safe and reliable way.
    """
    extracted = []
    text_upper = text.upper()

    for test in KNOWN_TESTS:
        # Pattern: Test name followed by optional symbols (<, >) and a number
        pattern = rf"{test}\s*([<>]?)\s*([\d,]+\.?\d*)"
        match = re.search(pattern, text_upper)

        if not match:
            continue

        symbol = match.group(1)
        raw_value = match.group(2).replace(",", "")

        try:
            value = float(raw_value)
        except ValueError:
            continue

        # Determine comparison type
        if symbol == "<":
            comparison = "less_than"
        elif symbol == ">":
            comparison = "greater_than"
        else:
            comparison = "exact"

        extracted.append({
            "test": test.title(),
            "value": value,
            "comparison": comparison,
            "raw_match": match.group(0)
        })

    return extracted
