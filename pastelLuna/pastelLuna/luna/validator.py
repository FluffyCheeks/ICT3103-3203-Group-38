from math import prod
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

def validate_product(request, imgname, productname, productdesc, unit, stock, cat, ingredients):

    check_imgname = check_input_len_validation(request, imgname, 8)
    check_productname = check_special_name(request, productname)
    check_productdesc = check_special_desc(request, productdesc)
    check_productingre = check_special_desc(request, ingredients)
    check_unit = check_number_unit(request, unit)
    check_stock = check_number_stock(request, stock)
    check_cat = check_number_cat(request, cat)

    if check_imgname == True and check_productname == True and check_productdesc == False and check_stock == False and check_unit==False and check_cat==False and check_productingre==False:
        return True
    else:
        return False