from django.contrib import messages
from django.core.exceptions import ValidationError
from password_strength import PasswordPolicy #added this to check for password complexity (fumin)






errorMsg = "not a valid phone no"


def raise_error(request, inputValue, errorMsg, subError):
    messages.error(request, ValidationError('%(value)s is %(error_msg)s - %(sub_error)s',
                                            params={'value': inputValue, 'error_msg': errorMsg,
                                                    'sub_error': subError}))

def raise_error_registration(request, subError):
    messages.error(request, ValidationError('%(sub_error)s',
    params={'sub_error': subError}))


# validate with len
def check_input_len_validation(request, inputValue, expLenNo):
    if len(inputValue) != expLenNo:
        subError = "Should contain 8 digits"
        raise_error(request, inputValue, errorMsg, subError)
        return True
    else:
        return False


# validate with contain alpha?
def check_input_contains_alpha_validation(request, inputValue):
    if any(c.isalpha() for c in inputValue):
        subError = "should not contain alphabet"
        raise_error(request, inputValue, errorMsg, subError)
        return True
    else:
        return False


def check_input_whitespace_validation(request, inputValue):
    res = " " in inputValue
    # by default set to false. if true got space
    if res == True:
        subError = "should not contain spaces"
        raise_error(request, inputValue, errorMsg, subError)
        return True
    else:
        return False


def check_input_special_char_validation(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "should not contain special characters"
        raise_error(request, inputValue, errorMsg, subError)
        return True
    else:
        return False

# Added policy.test function 26 Oct 2022, 12:34am (fumin)
#added this to check for password complexity (fumin)
# can change according to our needs
policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)

def check_pwd_match(request, inputValue, inputValue2):
    if (inputValue) != (inputValue2):
        subError = "Passwords do not match"
        raise_error_registration(request, subError)
        return False
    else:
        pwdvalidationtest = policy.test(inputValue2)
        #policy.test will return [] empty list if password is okay. Hence we want to test for empty list
        if len(pwdvalidationtest) == 0:  #means list is empty, so we can return True
            return True
        else:
            subError = "Passwords do not match requirements"
            raise_error_registration(request, subError)
            return False

#Added this 15 Oct 22, 11:43PM  (fumin)
def check_specialchar_fn(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "First Name should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True

#Added this 15 Oct 22, 11:43PM  (fumin)
def check_specialchar_ln(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "Last Name should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True

#Added this 15 Oct 22, 11:43PM  (fumin)
def check_specialchar_al(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "Allergies should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True

        
def check_special_name(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Name should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True

def check_special_desc(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Product Description should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True

def check_number_unit(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Unit should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True

def check_number_stock(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Stock should not have special characters"
        raise_error_registration(request, subError)
        return False
    elif any(c.isalpha() for c in value):
        subError = "Stock should not contain alphabet"
        raise_error(request, value, errorMsg, subError)
        return False
    else:
        return True


def check_number_cat(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Stock should not have special characters"
        raise_error_registration(request, subError)
        return False
    elif any(c.isalpha() for c in value):
        subError = "Stock should not contain alphabet"
        raise_error(request, value, errorMsg, subError)
        return False
    else:
        return True