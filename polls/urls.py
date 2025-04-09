from django.urls import path
from .views import home, about, donor_registration, search, search_info, contact, blood_availability
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('donor_registration/', donor_registration,
         name='donor_registration'),
    path('donor_registration/donor_list/',
         donor_registration, name='donor_list'),
    path('search/', search, name='search'),
    path('search_list/', search, name='search_list'),
    path('search/search_list/search_info/<int:donor_id>/',
         search_info, name='search_info'),
    path('contact/', contact, name='contact'),
    path('donor/<int:donor_id>/history/', views.donor_history, name='donor_history'),
    path('donor/<int:donor_id>/eligibility/', views.check_eligibility, name='check_eligibility'),
    path('donor/<int:donor_id>/record-donation/', views.record_donation, name='record_donation'),
    path('blood-availability/', views.blood_availability, name='blood_availability'),
    path('donor/<int:donor_id>/profile/', views.donor_profile, name='donor_profile'),
    path('all-donors/', views.all_donors, name='all_donors'),
]
