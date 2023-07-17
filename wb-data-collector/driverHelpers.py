"""
Helper functions for wb-data-collector driver
"""

"""
validIntInput

takes in an input, low bound, and high bound and validates whether the input is an int
and within the stated bounds
"""

def validIntInput(input, low_bound, high_bound):
    if input.isdigit:
        converted_input = int(input)
        if low_bound <= converted_input <= high_bound:
            return True
    return False