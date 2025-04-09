from django.contrib import admin
from . import models
# Register your models here.

class Register(admin.ModelAdmin):
    list_display = ['name', 'blood_group', 'state', 'city', 'home_address']

admin.site.register(models.donor_Registration, Register)

admin.site.register(models.sea_rch)

class Contact(admin.ModelAdmin):
    list_display = ['name', 'email']

admin.site.register(models.con_tact, Contact)

from .models import BloodInventory

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'component_type', 'quantity', 'donation_date', 'expiry_date', 'status')
    list_filter = ('blood_group', 'component_type', 'status')
    search_fields = ('blood_group', 'component_type', 'donor__name')
    date_hierarchy = 'donation_date'
    ordering = ('-created_at',)


