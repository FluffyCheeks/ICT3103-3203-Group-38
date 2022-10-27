from .error_list import *


def validate_phone_input(request, value, original_value):
    check_error_1 = check_input_len_validation(request, value, 8)
    check_error_2 = check_input_contains_alpha_validation(request, value)
    check_error_3 = check_input_whitespace_validation(request, value)
    check_error_4 = check_input_special_char_validation(request, value)

    if check_error_1 == False and check_error_2 == False and check_error_3 == False and check_error_4 == False:
        return False
    else:
        return original_value


def validate_name(request, fn, ln, fn_original_value, ln_original_value):
    check_fn = check_specialchar_fn(request, fn)
    check_ln = check_specialchar_ln(request, ln)
    if check_fn == True and check_ln == True:
        return False
    else:
        return fn_original_value, ln_original_value


def validate_allergies(request, al, al_original_value):
    check_al = check_specialchar_al(request, al)
    if check_al:
        return False
    else:
        return al_original_value


def validate_address(request, ad, ad_original_value):
    #check_ad = check_specialchar_ad(request, ad)

    return False


def registration_validation(request, fn, ln, al, pwd, cfm_pwd):
    check_fn = check_specialchar_fn(request, fn)
    check_ln = check_specialchar_ln(request, ln)
    check_al = check_specialchar_al(request, al)
    check_pwd = check_pwd_match(request, pwd, cfm_pwd)

    if check_fn == True and check_ln == True and check_al == True and check_pwd == True:
        messages.success(request, 'Registration Successful')
        return True
    else:
        return False
