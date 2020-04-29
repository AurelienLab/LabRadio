def bit_to_mb(value):
    value_mb_int = value / 1000000

    return round(value_mb_int, 2)  # Result rounded to 2 digits


def bit_to_mb_str(value):
    return str(bit_to_mb(value))  # Converts float result to string
