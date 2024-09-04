from django.urls import path

from . import views


urlpatterns = [
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('register/', views.register, name='register'),
  path('/', views.dashboard, name='account'),
]