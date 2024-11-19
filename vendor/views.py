from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import  UserProfile
from .models import Vendor
from menu.models import Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.forms import CategoryForm
from django.utils.text import slugify
# Create your views here.

def get_vendor(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    return vendor
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

def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor)
    
    
    context = { 'categories': categories}
    return render(request, 'vendor/menu-builder.html', context) 

def fooditems_by_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category, pk=pk)
    print(vendor, vendor.id)
    print(category, category.id)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    print('fooditem by category',vendor, category, fooditems)
    context = { 'fooditems': fooditems,
                'category': category}
    print('werewr',fooditems)
    return render (request,'vendor/food-items.html', context)

def add_category(request):
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            form  = form.save(commit=False)
            form.vendor = get_vendor(request)
            form.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {'form':form}
    return render(request, 'vendor/add-category.html', context)

def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    print('edit cat:')
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance = category)
        if form.is_valid():
            category = Category.objects.get(pk=pk)
            cleaned_data = form.clean()
            category.category_name = cleaned_data['category_name']
            category.description = cleaned_data['description']
            category.save()
            messages.success(request, 'Category updated successfully')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {'form':form,
               'category': category,
               }
    return render(request, 'vendor/edit-category.html', context)

def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('menu_builder')