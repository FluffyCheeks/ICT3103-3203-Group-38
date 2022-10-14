from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from string import ascii_letters, digits

errorMsg = "not a valid phone no"


def raise_error(request, inputValue, errorMsg, subError):
    messages.error(request, ValidationError('%(value)s is %(error_msg)s - %(sub_error)s',
                                            params={'value': inputValue, 'error_msg': errorMsg,
                                                    'sub_error': subError}))


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
    if set(inputValue).difference(ascii_letters + digits):
        subError = "should not contain special characters"
        raise_error(request, inputValue, errorMsg, subError)
        return True
    else:
        return False
