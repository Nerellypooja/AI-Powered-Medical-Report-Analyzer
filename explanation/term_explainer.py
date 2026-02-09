import json

def load_term_definitions(path="data/medical_terms.json"):
    with open(path, "r") as f:
        return json.load(f)

def explain_term(test_name):
    terms = load_term_definitions()
    return terms.get(
        test_name,
        "This test provides information about your blood health."
    )
