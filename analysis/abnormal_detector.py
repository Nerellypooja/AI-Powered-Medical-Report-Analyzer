import json

from parser.unit_normalizer import normalize_value

def load_ranges(path="data/medical_ranges.json"):
    with open(path, "r") as f:
        return json.load(f)

def detect_abnormal(labs, gender="male"):
    """
    Determines whether lab values are LOW / NORMAL / HIGH
    """
    ranges = load_ranges()
    results = []

    for lab in labs:
        test = lab["test"]
        value = normalize_value(test, lab["value"])
        comparison = lab["comparison"]

        if test not in ranges:
            continue

        ref = ranges[test]

        # Choose range based on gender or common
        if gender in ref:
            low, high = ref[gender]
        else:
            low, high = ref["all"]

        status = "Normal"

        if comparison == "less_than":
                status = "Normal"
        elif comparison == "greater_than":
            if value >= high:
                status = "Normal"
            else:
                status = "Low"
        else:
            if value < low:
                status = "Low"
            elif value > high:
                status = "High"

        results.append({
            "test": test,
            "value": value,
            "status": status,
            "normal_range": f"{low} – {high} {ref['unit']}"
        })

    return results
