from django.contrib import messages
from django.core.exceptions import ValidationError
from password_strength import PasswordPolicy #added this to check for password complexity (fumin)
from PIL import Image




errorMsg = "not a valid phone no"
errorMsgPhone = "not a valid phone no"
errorMsgAddress = "not a valid address"


def raise_error(request, inputValue, errorMsg, subError):
    messages.error(request, ValidationError('%(value)s is %(error_msg)s - %(sub_error)s',
                                            params={'value': inputValue, 'error_msg': errorMsg,
                                                    'sub_error': subError}))


def raise_error_registration(request, subError):
    messages.error(request, ValidationError('%(sub_error)s',
                                            params={'sub_error': subError}))

def raise_error_editor(request, subError):
    messages.error(request, ValidationError('%(sub_error)s',
    params={'sub_error': subError}))


# CHECKING FOR PHONE (len)
def check_input_len_validation(request, inputValue, expLenNo):
    if inputValue == 'None':
        return False
    if inputValue == "":
        return False
    else:
        if len(inputValue) != expLenNo:
            subError = "Should contain ", expLenNo, " digits"
            raise_error(request, inputValue, errorMsgPhone, subError)
            return True
        else:
            return False


# CHECKING FOR PHONE WITH NO ALPHABET
def check_input_contains_alpha_validation(request, inputValue):
    if inputValue == 'None':
        return False
    else:
        if any(c.isalpha() for c in inputValue):
            subError = "should not contain alphabet"
            raise_error(request, inputValue, errorMsgPhone, subError)
            return True
        else:
            return False


# CHECKING FOR PHONE WHITESPACE
def check_input_whitespace_validation(request, inputValue):
    res = " " in inputValue
    if inputValue == 'None':
        return False
    else:
        if res == True:
            subError = "should not contain spaces"
            raise_error(request, inputValue, errorMsgPhone, subError)
            return True
        else:
            return False


# CHECKING FOR PHONE SPECIAL CHAR
def check_input_special_char_validation(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "should not contain special characters"
        raise_error(request, inputValue, errorMsgPhone, subError)
        return True
    else:
        return False


# CHECKING FOR ADDRESS EMPTY FIELDS BACKEND
def check_empty_fields(request, arr):
    for i in arr:
        if len(i) == 0:
            subError = "should not leave any blanks"
            inputValue = "NULL fields"
            raise_error(request, inputValue, errorMsgAddress, subError)
            return False
        else:
            return True


# CHECKING FOR ADDRESS POSTAL CODE
def check_postal_code(request, PostalCode):
    if len(PostalCode) == 6 and PostalCode.isdigit() == True:
        return True
    else:
        subError = "postal code should contains 6 digits"
        raise_error(request, PostalCode, errorMsgAddress, subError)
        return False


# CHECKING FOR ADDRESS UNIT NUMBER
def check_unit_no(request, UnitNumber):
    if UnitNumber.isdigit():
        return True
    else:
        subError = "unit number should contains only numbers"
        raise_error(request, UnitNumber, errorMsgAddress, subError)
        return False


# CHECKING FOR ADDRESS STREET NAME
def check_street_name(request, StreetName):
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in StreetName):
        subError = "should not contain special characters"
        raise_error(request, StreetName, errorMsgAddress, subError)
        return False
    else:
        return True


# CHECKING FOR ADDRESS BLK NO if string contains blk
def check_blk_no(request, BlockNumber):
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in BlockNumber):
        subError = "should not contain special characters"
        raise_error(request, BlockNumber, errorMsgAddress, subError)
        return False
    else:
        temp_arr = [BlockNumber[0], BlockNumber[1], BlockNumber[2]]
        if any(c.isalpha() for c in temp_arr):
            subError = "first three letters cannot be alphabet"
            raise_error(request, BlockNumber, errorMsgAddress, subError)
            return False
        else:
            return True


def check_unit_lvl(request, UnitLevel):
    if int(UnitLevel) < 0:
        subError = "unit level is not in the range of 0-100"
        raise_error(request, UnitLevel, errorMsgAddress, subError)
        return False
    elif int(UnitLevel) > 100:
        subError = "unit level is not in the range of 0-100"
        raise_error(request, UnitLevel, errorMsgAddress, subError)
        return False
    else:
        return True

# Added policy.test function 26 Oct 2022, 12:34am (fumin)
# added this to check for password complexity (fumin)
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
        # policy.test will return [] empty list if password is okay. Hence we want to test for empty list
        if len(pwdvalidationtest) == 0:  # means list is empty, so we can return True
            return True
        else:
            subError = "Passwords do not match requirements"
            raise_error_registration(request, subError)
            return False


# Added this 15 Oct 22, 11:43PM  (fumin)
def check_specialchar_fn(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "First Name should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True


# Added this 15 Oct 22, 11:43PM  (fumin)
def check_specialchar_ln(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "Last Name should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True


# Added this 15 Oct 22, 11:43PM  (fumin)
def check_specialchar_al(request, inputValue):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in inputValue):
        subError = "Allergies should not have special characters"
        raise_error_registration(request, subError)
        return False
    else:
        return True

#Product errors        
def check_special_name(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Name should not have special characters"
        raise_error_editor(request, subError)
        return False
    else:
        return True

def check_special_desc(request, value):
    # OWASP recommends special char list
    special_characters = "\"#$%&'()*+/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Product Description should not have special characters"
        raise_error_editor(request, subError)
        return False
    else:
        return True

def check_number_unit(request, value):
    # OWASP recommends special char list
    special_characters = "e!\"#$%&'()*+-/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Unit should not have special characters"
        raise_error_editor(request, subError)
        return False
    else:
        return True

def check_number_stock(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Stock should not have special characters"
        raise_error_editor(request, subError)
        return False
    elif any(c.isalpha() for c in value):
        subError = "Stock should not contain alphabet"
        raise_error(request, value, errorMsg, subError)
        return False
    else:
        return True


def check_special_cat(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+/:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Category should not have special characters"
        raise_error_editor(request, subError)
        return False
    else:
        return True

def check_input_length(request, inputValue, expLenNo):
    special_characters = "!\"#$%&'()*+/:;<=>?@[\]^_`{|}~"
    if len(inputValue) > expLenNo:
        print(len(inputValue))
        subError = "Product Name should only have maximum of " + expLenNo + " characters"
        raise_error(request, inputValue, errorMsg, subError)
        return False
    elif any(c in special_characters for c in inputValue):
        subError = "Product Name/ Description should not have special characters"
        raise_error_editor(request, subError)
        return False
    else:
        return True

def check_image_file(request, image):
    i=Image.open(image)
    if i.format !='JPEG':
        subError = "Image should only be in .Jpg format"
        raise_error_editor(request, subError)
        return False
    elif i == None:
        subError = "Error in Uploading File"
        raise_error_editor(request, subError)
        return False
    else:
        return True


#LOGIN
def check_special_name(request, value):
    # OWASP recommends special char list
    special_characters = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~"
    if any(c in special_characters for c in value):
        subError = "Name should not have special characters"
        raise_error_editor(request, subError)
        return False
    else:
        return True