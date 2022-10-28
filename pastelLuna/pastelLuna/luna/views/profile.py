from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render


from luna.models import *
from luna.validator import *


def profile(request):
    # inner join with id where user id =1 (pass in through param)
    global res_validate_address
    obj = Users.objects.select_related("role_id").filter(id=1896)

    if request.method == 'POST':
        editProfile = Users.objects.get(id=1896)
        if request.POST.get('save', '') == 'update':
            get_building_type = request.POST.get('colorRadio')  # either hdb or lp

            if get_building_type == "LP":
                # backend validation set lp as required fields, and validate each fields
                res_validate_address = validate_address_lp(request,
                                                           request.POST.get('UnitNumber_lp'),
                                                           request.POST.get('PostalCode_lp'),
                                                           request.POST.get('StreetName_lp'),
                                                           editProfile.address)
            elif get_building_type == "HDB":
                # backend validation set hdb as required fields, and validate each fields
                res_validate_address = validate_address_hdb(request,
                                                            request.POST.get('BlockNumber'),
                                                            request.POST.get('UnitLevel'),
                                                            request.POST.get('UnitNumber'),
                                                            request.POST.get('PostalCode'),
                                                            request.POST.get('StreetName'),
                                                            editProfile.address)
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
                    final_address = request.POST.get('UnitNumber_lp') + " " + request.POST.get(
                        'StreetName_lp') + " Singapore " + request.POST.get('PostalCode_lp')
                    editProfile.address = final_address

                elif get_building_type == "HDB":
                    final_address = request.POST.get('BlockNumber') + " " + request.POST.get(
                        'StreetName') + " # " + request.POST.get('UnitLevel') + "-" + \
                                    request.POST.get('UnitNumber') + " " + "Singapore " + request.POST.get(
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
        context = {"object": obj}
        return render(request, "profile.html", context)
