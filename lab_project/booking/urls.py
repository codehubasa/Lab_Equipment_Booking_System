from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('book_lab/', views.book_lab, name='book_lab'),
    path('book/<int:id>/', views.book_equipment, name='book_equipment'),
    path('success/', views.success, name='success'),
    path('lab_success/', views.lab_success, name='lab_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('approve/<str:stype>/<int:id>/', views.approve_booking, name='approve_booking'),
    path('reject/<str:stype>/<int:id>/', views.reject_booking, name='reject_booking'),
    path('return/<int:id>/', views.return_equipment, name='return_equipment'),
]