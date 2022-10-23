from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from luna.models import *
from luna.validator import *

@csrf_exempt
def profile(request):
    # inner join with id where user id =1 (pass in through param)
    obj = Users.objects.select_related("role_id").filter(id=1)

    if request.method == 'POST':
        editProfile = Users.objects.get(id=1)
        if request.POST.get('save', '') == 'update':
            editProfile.first_name = request.POST.get('firstname')
            editProfile.last_name = request.POST.get('lastname')
            # input validation for phone textbox
            if not validate_phone_input(request, request.POST.get('mobile'), editProfile.phone):
                editProfile.phone = request.POST.get('mobile')
            # TODO input validation for address text box
            editProfile.address = request.POST.get("address")
            editProfile.allergies = request.POST.get("allergies")
            # Save to the database here
            editProfile.save()
            return HttpResponseRedirect(request.path_info)
    else:
        context = {"object": obj}
        return render(request, "profile.html", context)
