from .error_list import *


def validate_phone_input(value):
    error = "not a valid phone number"
    check_error_1 = check_input_len_validation(value, 8, error)
    check_error_2 = check_input_contains_alpha_validation(value, error)
    check_error_3 = check_input_whitespace_validation(value, error)
    check_error_4 = check_input_special_char_validation(value, error)

    if check_error_1 == False & check_error_2 == False & check_error_3 == False & check_error_4 == False:
        return False
