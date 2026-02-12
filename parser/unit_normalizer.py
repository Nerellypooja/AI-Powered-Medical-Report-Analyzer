def normalize_value(test_name, value):
    name = test_name.lower()

    # Platelets
    if name == "platelet count":
        if value < 10:
            return value * 100000
        elif value < 1000:
            return value * 1000
        return value

    # WBC
    if name == "total leukocyte count":
        if value < 100:
            return value * 1000
        return value

    # RBC
    if name == "rbc count":
        if value > 1000:
            return value / 1000000
        return value

    return value
