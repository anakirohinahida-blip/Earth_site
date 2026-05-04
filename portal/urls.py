from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('apple/', views.apple, name='apple'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('locations/', views.locations, name='locations'),
    path('contact/', views.contact, name='contact'),
    path('personal_account/', views.profile, name='personal_account'),
]