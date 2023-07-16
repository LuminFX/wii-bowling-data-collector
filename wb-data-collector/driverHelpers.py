def validIntInput(input, low_bound, high_bound):
    if input.isdigit:
        converted_input = int(input)
        if low_bound <= converted_input <= high_bound:
            return True
    return False