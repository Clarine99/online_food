from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import  UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    print('in vprofile!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if request.method == 'POST':
        print('request posted (in vProfile)')
        profile_form = UserProfileForm(request.POST, request.FILES, instance= profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            print('validdddd (in vprofile)')
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('vProfile')
        
        else:
            print(profile_form['profile_pic'].errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form':profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' : vendor
    }
    return render( request, 'vendor/vProfile.html', context)