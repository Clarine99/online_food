
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from accounts import views as acc_views

urlpatterns = [
   path('', acc_views.vendorDashboard, name='vProfile'),
   path('profile/', views.vProfile, name='vProfile'),
]
