import json
from parser.unit_normalizer import normalize_value

def load_ranges(path="data/medical_ranges.json"):
    with open(path, "r") as f:
        return json.load(f)

def detect_abnormal(labs, gender="male"):
    ranges = load_ranges()
    results = []

    for lab in labs:
        test = lab["test"]
        value = lab["value"]
        comparison = lab["comparison"]

        if test not in ranges:
            continue

        # Normalize value first
        value = normalize_value(test, value)

        ref = ranges[test]

        # Special case: HbA1c
        if test == "HbA1c":
            if value < ref["normal"][1]:
                status = "Normal"
                low, high = ref["normal"]
            elif value < ref["prediabetes"][1]:
                status = "High"
                low, high = ref["prediabetes"]
            else:
                status = "High"
                low, high = ref["diabetes"]
        else:
            if gender in ref:
                low, high = ref[gender]
            else:
                low, high = ref["all"]

            status = "Normal"
            if comparison == "less_than":
                status = "Normal" if value <= low else "High"
            elif comparison == "greater_than":
                status = "High" if value >= high else "Normal"
            else:
                if value < low:
                    status = "Low"
                elif value > high:
                    status = "High"

        is_suspicious = value > (high * 10)

        results.append({
            "test": test,
            "value": value,
            "status": status,
            "normal_range": f"{low} – {high} {ref['unit']}",
            "is_suspicious": is_suspicious
        })

    return results
