from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from luna.models import *
from luna.validator import *


def profile(request):
    # inner join with id where user id =1 (pass in through param)
    obj = Users.objects.select_related("role_id").filter(id=1896)

    if request.method == 'POST':
        editProfile = Users.objects.get(id=1896)
        if request.POST.get('save', '') == 'update':
            res_validate_name = validate_name(request, request.POST.get('firstname'), request.POST.get('lastname'),
                                              editProfile.first_name, editProfile.last_name)
            res_validate_phone = validate_phone_input(request, request.POST.get('mobile'), editProfile.phone)
            res_validate_allergies = validate_allergies(request, request.POST.get('allergies'), editProfile.allergies)
            res_validate_address = validate_address(request, request.POST.get('address'), editProfile.address)

            if res_validate_name == False and res_validate_phone == False and res_validate_allergies == False and res_validate_address == False:
                editProfile.first_name = request.POST.get('firstname')
                editProfile.last_name = request.POST.get('lastname')
                editProfile.phone = request.POST.get('mobile')
                editProfile.address = request.POST.get("address")
                editProfile.allergies = request.POST.get("allergies")
                messages.success(request, 'Profile Update Successful')

            editProfile.save()
            return HttpResponseRedirect(request.path_info)
    else:
        context = {"object": obj}
        return render(request, "profile.html", context)
