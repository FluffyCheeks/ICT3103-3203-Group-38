from .error_list import *


def validate_phone_input(request, value, original_value):
    check_error_1 = check_input_len_validation(request, value, 8)
    check_error_2 = check_input_contains_alpha_validation(request, value)
    check_error_3 = check_input_whitespace_validation(request, value)
    check_error_4 = check_input_special_char_validation(request, value)

    if check_error_1 == False and check_error_2 == False and check_error_3 == False and check_error_4 == False:
        messages.success(request, 'Profile updated successfully')
        return False
    else:
        return original_value
