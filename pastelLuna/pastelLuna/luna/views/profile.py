from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.html import escape

from luna.models import *
from luna.validator import *
from luna.streets import *
from luna.allergies import *

@sensitive_variables('id')
def check_for_cookie_session(request):
    try:
        id = request.session['role_id_id']
        return id
    except:
        var = False
        return var


@sensitive_post_parameters()
def res_validate_address_LP(request, address_origin):
    res_validate_address = validate_address_lp(request,
                                               escape(request.POST.get('UnitNumber_lp')),
                                               escape(request.POST.get('PostalCode_lp')),
                                               escape(request.POST.get('StreetName_lp')),
                                               escape(address_origin))
    return res_validate_address


def res_validate_address_HDB(request, address_origin):
    res_validate_address = validate_address_hdb(request,
                                                escape(request.POST.get('BlockNumber')),
                                                escape(request.POST.get('UnitLevel')),
                                                escape(request.POST.get('UnitNumber')),
                                                escape(request.POST.get('PostalCode')),
                                                escape(request.POST.get('StreetName')),
                                                escape(address_origin))
    return res_validate_address


def leading_zero_no(number):
    if len(number) == 1:
        store = str(number).zfill(2)
    else:
        store = number

    return store


@sensitive_post_parameters()
@sensitive_variables('uid')
def profile(request):
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 1:
        uid = request.session['id']
        num_cart = showcart_base(request) 

        json_data = street_name_list()
        json_data_al = allergies_list()
        global res_validate_address

        obj = Users.objects.select_related("role_id").filter(id=uid)
        if request.method == 'POST':
            editProfile = Users.objects.get(id=uid)
            if request.POST.get('save', '') == 'update':
                if editProfile.email_valid == False:
                    messages.error(request, 'Profile update not successful. email is not valid. contact admin@pastelluna.com.')
                    return redirect("profile")


                some_var_allergies = request.POST.getlist('allergy')
                joined_string_allergies = ", ".join(some_var_allergies)

                get_building_type = request.POST.get('colorRadio')  # either hdb or lp

                if get_building_type == "LP":
                    # backend validation set lp as required fields, and validate each fields
                    res_validate_address = res_validate_address_LP(request, escape(editProfile.address))
                elif get_building_type == "HDB":
                    # backend validation set hdb as required fields, and validate each fields
                    res_validate_address = res_validate_address_HDB(request, escape(editProfile.address))
                else:
                    res_validate_address = False

                res_validate_name = validate_name(request,
                                                  escape(request.POST.get('firstname')),
                                                  escape(request.POST.get('lastname')),
                                                  escape(editProfile.first_name),
                                                  escape(editProfile.last_name))
                res_validate_phone = validate_phone_input(request,
                                                          escape(request.POST.get('mobile')),
                                                          escape(editProfile.phone))
                res_validate_allergies = validate_allergies(request,
                                                            escape(request.POST.get('allergies')),
                                                            escape(editProfile.allergies))

                if res_validate_name == False and res_validate_phone == False and res_validate_allergies == False and res_validate_address == False:
                    if get_building_type == "LP":
                        final_address = leading_zero_no(escape(request.POST.get('UnitNumber_lp'))) + " " + escape(
                            request.POST.get(
                                'StreetName_lp')) + " Singapore " + escape(request.POST.get('PostalCode_lp'))
                        editProfile.address = escape(final_address)

                    elif get_building_type == "HDB":
                        final_address = escape(request.POST.get('BlockNumber')) + " " + escape(request.POST.get(
                            'StreetName')) + " # " + leading_zero_no(escape(request.POST.get('UnitLevel'))) + "-" + \
                                        leading_zero_no(
                                            escape(request.POST.get('UnitNumber'))) + " " + "Singapore " + escape(
                            request.POST.get(
                                'PostalCode'))
                        editProfile.address = escape(final_address)

                    editProfile.first_name = escape(request.POST.get('firstname'))
                    editProfile.last_name = escape(request.POST.get('lastname'))
                    editProfile.phone = escape(request.POST.get('mobile'))
                    editProfile.allergies = escape(joined_string_allergies)
                    messages.success(request, 'Profile Update Successful')

                editProfile.save()
                return HttpResponseRedirect(request.path_info)
        else:
            return render(request, "profile.html", {'object': obj, 'yb': json_data['streetName'],'products_num': num_cart})
    else:
        return render(request, "unauthorised_user.html")


def showcart_base(request):
    # needs to add into session
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 1:
        uid = escape(request.session['id'])
        num_of_prod = Cart.objects.filter(user_id=uid)
        print(num_of_prod.count, "---- COUNTR")
        return num_of_prod.count
    else:
        num_of_prod = 0
        return num_of_prod