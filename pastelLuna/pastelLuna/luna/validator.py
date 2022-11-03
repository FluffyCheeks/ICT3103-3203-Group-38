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


def registration_validation(request, fn, ln, em, al, pwd, cfm_pwd):
    check_fn = check_specialchar_fn(request, fn)
    check_fn_num = check_numeric_fn(request, fn)
    check_ln = check_specialchar_ln(request, ln)
    check_ln_num = check_numeric_ln(request, ln)
    check_em = check_specialchar_email(request, em)
    check_al = check_specialchar_al(request, al)
    check_al_num = check_numeric_al(request, al)
    check_pwd = check_pwd_match(request, pwd, cfm_pwd)

    if check_fn == True and check_fn_num == True and check_ln == True and check_ln_num == True and check_al == True and check_al_num == True and check_em == True and check_pwd == True:
        return True
    else:
        return False

def otp_check_sanitize(request, otp):
    check_otp = check_specialchar_otp(request,otp)
    check_otp_alpha = check_otp_contains_alpha_validation(request,otp)
    
    if check_otp == True and  check_otp_alpha == True:
        return True
    else:
        return False
