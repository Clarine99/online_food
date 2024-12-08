
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from accounts import views as acc_views

urlpatterns = [
   path('', acc_views.vendorDashboard, name='vProfile'),
   path('profile/', views.vProfile, name='vProfile'),
   path('menu-builder/', views.menu_builder, name='menu_builder'),
   path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
   path('menu-builder/add-category/', views.add_category, name='add_category'),
   path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
   path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
   path('menu-builder/add/', views.add_food,  name='add_food'),
   path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
   path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),
   

   

]
