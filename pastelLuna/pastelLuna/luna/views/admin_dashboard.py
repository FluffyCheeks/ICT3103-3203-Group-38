from datetime import datetime, timezone

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from luna.models import *
from luna.validator import *


def admin_dashboard(request):
    prod_req = Product_Request.objects.select_related("product_id", "user_id")
    uid = request.session['id']
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")

    # but need to tie back to the created and updated
    # admin only have one account so create a session for 1 account only
    if request.method == 'POST':
        if 'approve' in request.POST.values():
            try:
                get_selected_req_id = [key for key in request.POST.keys()][1]
                approve_prod_req = Product_Request.objects.get(id=get_selected_req_id)
                approve_prod_req.status = 'approve'
                approve_prod_req.updated = formatedDate
                approve_prod_req.save()
            except:
                messages.error(request, 'Product request not approved')

            messages.success(request, 'Product request approved successfully')

            return HttpResponseRedirect(request.path_info)
        elif 'reject' in request.POST.values():
            try:
                get_selected_req_id = [key for key in request.POST.keys()][1]
                reject_prod_req = Product_Request.objects.get(id=get_selected_req_id)
                reject_prod_req.status = 'reject'
                reject_prod_req.updated = formatedDate
                reject_prod_req.save()
            except:
                messages.error(request, 'Product request not rejected')

            messages.success(request, 'Product request rejected successfully')

            return HttpResponseRedirect(request.path_info)
    else:
        context = {"object": prod_req}
    return render(request, "admin_dashboard.html", context)
