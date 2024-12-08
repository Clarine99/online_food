from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import  UserProfile
from .models import Vendor
from menu.models import Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.forms import CategoryForm, FoodForm
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
   
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    
    context = { 'fooditems': fooditems,
                'category': category}
    
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
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    
    print(get_vendor(request))
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food  = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)+'-'+str(food.id)
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {'form':form}

    return render (request, 'vendor/add-food.html', context)


def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    print('edit cat:')
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance = food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)+'-'+str(food.id)
            form.save()
           
            messages.success(request, 'Category updated successfully')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = FoodForm(instance=food)
    context = {'form':form,
                'food': food,
               }
    print('[edit_food]: ',food)
    return render(request, 'vendor/edit_food.html', context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Thefood has been  deleted successfully')
    return redirect('menu_builder')