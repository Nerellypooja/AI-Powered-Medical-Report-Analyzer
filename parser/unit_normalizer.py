
# parser/unit_normalizer.py

def normalize_value(test_name, value):
    """
    Normalize lab values based on common medical reporting conventions.
    Returns corrected value.
    """

    test_name = test_name.upper()

    # Total Leukocyte Count sometimes written in thousands
    if test_name == "TOTAL LEUKOCYTE COUNT":
        if value < 100:
            return value * 1000

    # Other tests are usually already normalized
    return value
