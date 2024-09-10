from django.urls import path

from . import views


urlpatterns = [
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('register/', views.register, name='register'),
  path('resetPassword/', views.resetPassword, name='resetPassword'),
  path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
  path('', views.dashboard, name='account'),
]