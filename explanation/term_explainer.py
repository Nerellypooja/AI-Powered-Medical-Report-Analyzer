import json

def load_term_definitions(path="data/medical_terms.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def explain_term(test_name):
    terms = load_term_definitions()

    if not test_name:
        return "No explanation available."

    test_name_clean = test_name.strip().lower()

    # 1. Exact match
    for key, value in terms.items():
        if test_name_clean == key.lower():
            return value

    # 2. Partial match (handles Hb → Hemoglobin, etc.)
    for key, value in terms.items():
        if key.lower() in test_name_clean or test_name_clean in key.lower():
            return value

    # 3. Default fallback
    return "This test provides information about your health. Please consult your doctor for detailed advice."
