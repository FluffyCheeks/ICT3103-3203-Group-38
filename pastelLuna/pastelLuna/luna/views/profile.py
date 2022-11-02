from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from luna.models import *
from luna.validator import *
from luna.streets import *

def check_for_cookie_session(request):
    try:
        id = request.session['role_id_id']
        return id
    except:
        var = False
        return var

def res_validate_address_LP(request, address_origin):
    res_validate_address = validate_address_lp(request,
                                               request.POST.get('UnitNumber_lp'),
                                               request.POST.get('PostalCode_lp'),
                                               request.POST.get('StreetName_lp'),
                                               address_origin)
    return res_validate_address


def res_validate_address_HDB(request, address_origin):
    res_validate_address = validate_address_hdb(request,
                                                request.POST.get('BlockNumber'),
                                                request.POST.get('UnitLevel'),
                                                request.POST.get('UnitNumber'),
                                                request.POST.get('PostalCode'),
                                                request.POST.get('StreetName'),
                                                address_origin)
    return res_validate_address


def leading_zero_no(number):
    if len(number) == 1:
        store = str(number).zfill(2)
    else:
        store = number

    return store

def profile(request):
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 1:
        uid = request.session['id']

        json_data = street_name_list()

        global res_validate_address

        obj = Users.objects.select_related("role_id").filter(id=uid)
        if request.method == 'POST':
            editProfile = Users.objects.get(id=uid)
            if request.POST.get('save', '') == 'update':
                get_building_type = request.POST.get('colorRadio')  # either hdb or lp

                if get_building_type == "LP":
                    # backend validation set lp as required fields, and validate each fields
                    res_validate_address = res_validate_address_LP(request, editProfile.address)
                elif get_building_type == "HDB":
                    # backend validation set hdb as required fields, and validate each fields
                    res_validate_address = res_validate_address_HDB(request, editProfile.address)
                else:
                    res_validate_address = False

                res_validate_name = validate_name(request,
                                                  request.POST.get('firstname'),
                                                  request.POST.get('lastname'),
                                                  editProfile.first_name,
                                                  editProfile.last_name)
                res_validate_phone = validate_phone_input(request,
                                                          request.POST.get('mobile'),
                                                          editProfile.phone)
                res_validate_allergies = validate_allergies(request,
                                                            request.POST.get('allergies'),
                                                            editProfile.allergies)

                if res_validate_name == False and res_validate_phone == False and res_validate_allergies == False and res_validate_address == False:
                    if get_building_type == "LP":
                        final_address = leading_zero_no(request.POST.get('UnitNumber_lp')) + " " + request.POST.get(
                            'StreetName_lp') + " Singapore " + request.POST.get('PostalCode_lp')
                        editProfile.address = final_address

                    elif get_building_type == "HDB":
                        final_address = request.POST.get('BlockNumber') + " " + request.POST.get(
                            'StreetName') + " # " + leading_zero_no(request.POST.get('UnitLevel'))+ "-" + \
                                        leading_zero_no(request.POST.get('UnitNumber')) + " " + "Singapore " + request.POST.get(
                            'PostalCode')
                        editProfile.address = final_address

                    editProfile.first_name = request.POST.get('firstname')
                    editProfile.last_name = request.POST.get('lastname')
                    editProfile.phone = request.POST.get('mobile')
                    editProfile.allergies = request.POST.get("allergies")
                    messages.success(request, 'Profile Update Successful')

                editProfile.save()
                return HttpResponseRedirect(request.path_info)
        else:
            return render(request, "profile.html", {'object': obj, 'yb': json_data['streetName']})
    else:
        return render(request, "unauthorised_user.html")
