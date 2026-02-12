import re

ALIASED_TESTS = {
    # --- CBC ---
    "hemoglobin": "Hemoglobin",
    "hb": "Hemoglobin",
    "haemoglobin": "Hemoglobin",
    "hgb": "Hemoglobin",

    "total leukocyte count": "Total Leukocyte Count",
    "tlc": "Total Leukocyte Count",
    "wbc": "Total Leukocyte Count",
    "wbc count": "Total Leukocyte Count",

    "rbc": "RBC Count",
    "rbc count": "RBC Count",
    "total rbc count": "RBC Count",

    "platelet": "Platelet Count",
    "platelet count": "Platelet Count",
    "platelets": "Platelet Count",
    "plt": "Platelet Count",

    "hematocrit": "Hematocrit",
    "hct": "Hematocrit",
    "pcv": "Hematocrit",

    "mcv": "MCV",
    "mch": "MCH",
    "mchc": "MCHC",

    "neutrophils": "Neutrophils",
    "lymphocytes": "Lymphocytes",
    "monocytes": "Monocytes",
    "eosinophils": "Eosinophils",
    "basophils": "Basophils",

    # --- THYROID ---
    "thyroid stimulating hormone": "TSH",
    "tsh": "TSH",

    "triiodothyronine": "T3",
    "t3": "T3",
    "tt3": "T3",

    "thyroxine": "T4",
    "t4": "T4",
    "tt4": "T4",

    # --- DIABETES ---
    "hba1c": "HbA1c",
    "glycated hemoglobin": "HbA1c",

    # --- KIDNEY ---
    "creatinine": "Creatinine",
    "serum creatinine": "Creatinine",

    "urea": "Urea",
    "serum urea": "Urea",

    "bun": "BUN",

    "sodium": "Sodium",
    "serum sodium": "Sodium",

    "potassium": "Potassium",
    "serum potassium": "Potassium",

    "uric acid": "Uric Acid",
    "serum uric acid": "Uric Acid",

    "calcium": "Calcium",
    "calcium, total": "Calcium",

    "phosphorus": "Phosphorus",

    "egfr": "eGFR"
}


def parse_lab_values(text):
    extracted = []
    text_lower = text.lower()

    sorted_aliases = sorted(ALIASED_TESTS.keys(), key=len, reverse=True)

    for alias in sorted_aliases:
        pattern = rf"{re.escape(alias)}[\s\.\-\:]*([<>]?)\s*([\d,\.]+)"
        match = re.search(pattern, text_lower)

        if match:
            standard_name = ALIASED_TESTS[alias]
            symbol = match.group(1)
            raw_val = match.group(2).replace(",", "").strip(".")

            try:
                value = float(raw_val)

                extracted.append({
                    "test": standard_name,
                    "value": value,
                    "comparison": (
                        "less_than" if symbol == "<"
                        else "greater_than" if symbol == ">"
                        else "exact"
                    )
                })

                text_lower = text_lower.replace(match.group(0), "###", 1)

            except ValueError:
                continue

    return extracted
