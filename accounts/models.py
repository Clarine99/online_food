# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.dispatch import receiver
from django.db.models.fields.related import OneToOneField, ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserManager (BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Usermust have an email')
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.is_admin =True
        user.is_active = True
        user.is_staff= True
        user.is_superadmin = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1 
    CUSTOMER = 2

    ROLE_CHOICE = ((VENDOR, 'vendor'), (CUSTOMER,'customer'))

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=17, blank=True)
    role = models.PositiveSmallIntegerField (choices=ROLE_CHOICE, blank = True, null = True)

    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self) -> str:
        return self.username
    
    def has_perm (self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    def get_role(self):
        if self.role == 1:
            user_role = 'vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    
class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='media/users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='media/users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    
    
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    # location = gismodels.PointField(blank=True, null=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1} {self.address_line_2}'
    def __str__(self) -> str:
        return self.user.email
    
    # def save(self,*args, **kwargs):
    #     if self.longitude and self.latitude:
    #         self.location = Point(float(self.longitude),float(self.latitude))
    #         return super(UserProfile,self).save(*args, **kwargs)
            
    #     return super(UserProfile,self).save(*args, **kwargs)  



            


# post_save(created_user_profile_receiver, User)

