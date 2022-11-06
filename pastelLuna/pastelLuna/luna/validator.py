from math import prod
from .error_list import *
from pathlib import Path
from django.core.exceptions import ValidationError


# for profile phone
def validate_phone_input(request, value, original_value):
    check_error_1 = check_input_valid_number(request, value)
    check_error_2 = check_input_contains_alpha_validation(request, value)
    check_error_3 = check_input_whitespace_validation(request, value)
    check_error_4 = check_input_special_char_validation(request, value)

    print(check_error_1)
    if check_error_1 == False and check_error_2 == False and check_error_3 == False and check_error_4 == False:
        return False
    else:
        return original_value


# for profile name
def validate_name(request, fn, ln, fn_original_value, ln_original_value):
    check_fn = check_specialchar_fn(request, fn)
    check_ln = check_specialchar_ln(request, ln)
    check_fn_no = check_numeric_fn(request, fn)
    check_ln_no = check_numeric_ln(request, ln)

    if check_fn == True and check_ln == True and check_fn_no == True and check_ln_no == True:
        return False  # false as in no error
    else:
        return fn_original_value, ln_original_value


# for profile allergies
def validate_allergies(request, al, al_original_value):
    check_al = check_specialchar_al(request, al)
    check_al_no_num = check_numeric_al(request, al)
    if check_al == True and check_al_no_num == True:
        return False
    else:
        return al_original_value


# for profile address landed properties
def validate_address_lp(request, UnitNumber_lp, PostalCode_lp, StreetName_lp, address_original_value):
    arr = [UnitNumber_lp, PostalCode_lp, StreetName_lp]
    check_ef = check_empty_fields(request, arr)
    if check_ef == False:
        return address_original_value

    check_un = check_unit_no(request, UnitNumber_lp)
    check_pc = check_postal_code(request, PostalCode_lp)
    check_st = check_street_name(request, StreetName_lp)

    if check_ef == True and check_pc == True and check_un == True and check_st == True:
        return False
    else:
        return address_original_value


# for profile address hdb
def validate_address_hdb(request, BlockNumber, UnitLevel, UnitNumber, PostalCode, StreetName, address_original_value):
    arr = [BlockNumber, UnitLevel, UnitNumber, PostalCode, StreetName]
    check_ef = check_empty_fields(request, arr)
    if check_ef == False:
        return address_original_value

    check_bn = check_blk_no(request, BlockNumber)  # need to recheck this if possible
    check_ul = check_unit_lvl(request, UnitLevel)
    check_un = check_unit_no(request, UnitNumber)
    check_pc = check_postal_code(request, PostalCode)
    check_st = check_street_name(request, StreetName)

    if check_ef == True and check_bn == True and check_ul == True and check_pc == True and check_un == True and check_st == True:
        return False
    else:
        return address_original_value


# for registration
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
    check_otp = check_specialchar_otp(request, otp)
    check_otp_alpha = check_otp_contains_alpha_validation(request, otp)

    if check_otp == True and check_otp_alpha == True:
        return True
    else:
        return False

def validate_image(request, image):
    check_image = check_image_file(request, image)
    print(check_image,)
    if check_image == True:
        return True
    else:
        return False

def validate_product(request, imgname, productname, productdesc, unit, stock, cat, ingredients):
    check_imgname = check_input_length(request, imgname, 50)
    check_productname = check_special_name(request, productname)
    check_productdesc = check_special_desc(request, productdesc)
    check_productdesc_len = check_input_length(request, productdesc, 1000)
    check_productingre = check_special_desc(request, ingredients)
    check_unit = check_number_unit(request, unit)
    check_stock = check_number_stock(request, stock)
    check_cat = check_special_cat(request, cat)
    print(check_imgname, " ",check_productname, " ",check_productdesc , " ", check_productdesc_len  , " ",check_productingre , " ",check_stock  , " ", check_unit , " ", check_cat  , "", check_productingre)
    if check_imgname == True and check_productname == True and check_productdesc == True and check_productdesc_len == True and check_stock == True and check_unit==True and check_cat==True and check_productingre==True:
        return True
    else:
        return False

def validate_product_new(request, image, productname, productdesc, unit, stock, cat, ingredients):
    print("VALIDATING --", image)
    check_image = check_image_file(request, image)
    check_productname = check_special_name(request, productname)
    check_productdesc = check_special_desc(request, productdesc)
    check_productdesc_len = check_input_length(request, productdesc, 1000)
    check_productingre = check_special_desc(request, ingredients)
    check_unit = check_number_unit(request, unit)
    check_stock = check_number_stock(request, stock)
    check_cat = check_special_cat(request, cat)
    print(check_image, " ",check_productname, " ",check_productdesc , " ", check_productdesc_len  , " ",check_productingre , " ",check_stock  , " ", check_unit , " ", check_cat  , "", check_productingre)
    if check_image == True and check_productname == True and check_productdesc == True and check_productdesc_len == True and check_stock == True and check_unit==True and check_cat==True and check_productingre==True:
        return True
    else:
        return False