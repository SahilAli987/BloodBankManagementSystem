from django import forms
from django.forms import ModelForm
from . import models
from .models import BloodInventory


class DonorRegistration(ModelForm):
    class Meta:
        model = models.donor_Registration
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your Name'}),
            'father_name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your Father Name'}),
            'gender': forms.Select(
                attrs={'class': 'form-control', 'required': 'True'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your E-mail'}),
            'phone_number': forms.NumberInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your Phone Number'}),
            'state': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your State'}),
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your City'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control', 'required': 'True', 'type': 'date', 'max': 'today'}),
            'occupation': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your Occupation'}),
            'blood_group': forms.Select(
                attrs={'class': 'form-control', 'required': 'True'}),
            'home_address': forms.Textarea(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your Home Address'}),
            'last_donate_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'max': 'today'}),
            'weight': forms.NumberInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your Weight in kg', 'step': '0.1', 'min': '45'}),
            'any_disease': forms.Select(
                attrs={'class': 'form-control', 'required': 'True'}),
            'allergies': forms.Select(
                attrs={'class': 'form-control', 'required': 'True'}),
            'cardiac': forms.Select(
                attrs={'class': 'form-control', 'required': 'True'}),
            'bleeding_disorder': forms.Select(
                attrs={'class': 'form-control', 'required': 'True'}),
            'hbsAg_hcv_hIV': forms.Select(
                attrs={'class': 'form-control', 'required': 'True'}),
        }
        labels = {
            'date_of_birth': 'Date of Birth (YYYY-MM-DD)',
            'last_donate_date': 'Last Donation Date (YYYY-MM-DD)',
            'weight': 'Weight (kg)',
        }
        help_texts = {
            'date_of_birth': 'Enter your date of birth',
            'last_donate_date': 'Enter your last donation date if applicable',
            'weight': 'Minimum weight required: 45kg',
        }


class Search(forms.ModelForm):
    class Meta:
        model = models.sea_rch
        fields = '__all__'
        widgets = {'blood_group': forms.Select(
            attrs={'class': 'form-control', 'required': 'True'}),
            'state': forms.TextInput(
            attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your State'}),
            'city': forms.TextInput(
            attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Enter Your City'}),
        }


class Contact(forms.ModelForm):
    class Meta:
        model = models.con_tact
        fields = '__all__'
        widgets = {'name': forms.TextInput(
            attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Name'}),
            'phone_number': forms.NumberInput(
            attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(
            attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'E-mail'}),
            'subject': forms.Textarea(
            attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Subject...'}),
        }


class DonationHistoryForm(ModelForm):
    class Meta:
        model = models.DonationHistory
        fields = ['blood_volume', 'notes']
        widgets = {
            'blood_volume': forms.NumberInput(
                attrs={'class': 'form-control', 'required': 'True', 'placeholder': 'Blood volume in ml', 'step': '0.1'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Additional notes about the donation'}),
        }


class BloodAvailabilityFilter(forms.Form):
    blood_group = forms.ChoiceField(
        choices=BloodInventory.BLOOD_GROUPS,
        required=False,
        label='Blood Group',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_quantity = forms.IntegerField(
        required=False,
        label='Minimum Quantity (ml)',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    expiry_date = forms.DateField(
        required=False,
        label='Expiry Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=BloodInventory.STATUS_CHOICES,
        required=False,
        label='Status',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
