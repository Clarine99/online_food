from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import UserForm
from . models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from vendor.models import Vendor
from vendor.forms import VendorForm
from . utils import detect_role, send_verification_email # Create your views here.
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied('You must be a vendor to view this page') 
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied('You must be a customer to view this page')
def accounts(request):
    return HttpResponse('This is accounts page')
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
       
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()


            # using create_user() from models.py
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            mail_subject = "Please activate your account"
            mail_template = 'accounts/emails/verification_email.html'
            send_verification_email(request, user, mail_subject, mail_template)
            messages.success(request, " your account has been created successfully")
            print('form is saved....')
            return redirect ('login')
        else:
            print(form.errors)
           
            
            print('form is not valid....')
    else:
        form = UserForm()
  
    context = {'form':form}
     
    return render(request, 'accounts/userRegistration.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor =v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            mail_subject = "activate your account"
            email_template = "accounts/emails/verification_email.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "your account has been created successfully. Please wait for the approval.")
            return redirect('home')
            
        else:
            print(form.errors)
            print(v_form.errors)
    else:
        
        form = UserForm()
        v_form = VendorForm()
    context = {'form':form, 'v_form':v_form}
            
    return render(request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        user = None

    if User.id is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully')
        return redirect ('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect ('myAccount')
def login (request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        print('in login post')
        username = request.POST['email']
        password = request.POST['password']
        auth_user = auth.authenticate(request, username=username, password=password)
        if auth_user is not None:
            auth.login(request, auth_user)
            messages.success(request, 'you are logged in successfully')
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout (request):
    auth.logout(request)
    messages.info(request, 'you are logged out')
    return redirect('login')
def dashboard (request):
    user = request.user
    context = {'user':user}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url = 'login')
def myAccount(request):
    user = request.user
    print(f"views.myAccount: {user}")
    redirectUrl = detect_role(user)
    print(f"views.myAccount redirecturl: {redirectUrl}")
    
    
    return redirect(redirectUrl)

@login_required(login_url = 'login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    
    return render(request, 'accounts/vendorDashboard.html')

def forgot_password(request):
    # return HttpResponse('forgot password')
    if request.method == 'POST':
        
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            mail_subject = "Reset your  password"
            email_template = "accounts/emails/reset_password.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.warning(request, 'password reset link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect ('reset_password')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    return 

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password'] 
        if password == confirm_password:
            uid = request.session.get('uid')    
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'password does not match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')

