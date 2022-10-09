from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from string import ascii_letters, digits


def raise_error(inputValue, errorMsg):
    raise ValidationError(
        _('%(value)s is %(error_msg)s'),
        params={'value': inputValue, 'error_msg': errorMsg},
    )


# validate with len
def check_input_len_validation(inputValue, expLenNo, errorMsg):
    if len(inputValue) != expLenNo:
        raise_error(inputValue, errorMsg)
    else:
        return False


# validate with contain alpha?
def check_input_contains_alpha_validation(inputValue, errorMsg):
    if any(c.isalpha() for c in inputValue):
        raise_error(inputValue, errorMsg)
    else:
        return False


def check_input_whitespace_validation(inputValue, errorMsg):
    res = " " in inputValue
    # by default set to false. if true got space
    if res == True:
        raise_error(inputValue, errorMsg)
    else:
        return False


def check_input_special_char_validation(inputValue, errorMsg):
    if set(inputValue).difference(ascii_letters + digits):
        raise_error(inputValue, errorMsg)
    else:
        return False
