from django.shortcuts import render, redirect
from .forms import DonorRegistration, Contact, Search, DonationHistoryForm, BloodAvailabilityFilter
from .models import donor_Registration, sea_rch, con_tact, DonationHistory, BloodInventory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Q
from django.template import TemplateDoesNotExist


def home(request):
    if request.method == 'POST' and 'donor_id' in request.POST:
        donor_id = request.POST.get('donor_id')
        try:
            # Verify the donor exists
            donor = donor_Registration.objects.get(id=donor_id)
            # Redirect to the donor profile
            return redirect('donor_profile', donor_id=donor_id)
        except donor_Registration.DoesNotExist:
            messages.error(request, f"No donor found with ID {donor_id}")
    
    return render(request, 'polls/base.html')


def about(request):
    return render(request, 'polls/about.html')


def donor_registration(request):
    forms = DonorRegistration()
    if request.method == 'POST':
        forms = DonorRegistration(request.POST)
        if forms.is_valid():
            forms.save()
            context = {
                'forms': forms
            }

            return render(request, 'polls/donor_list.html', context)

        print(forms.errors)

    context_form = {
        'forms': forms
    }

    return render(request, 'polls/donor_registration.html', context_form)


def search(request):
    forms = Search()
    if request.method == 'POST':
        forms = Search(request.POST)
        if forms.is_valid():
            forms.save()
            bloodgroup = forms.cleaned_data['blood_group']
            state = forms.cleaned_data['state']
            city = forms.cleaned_data['city']
            donor_filter = donor_Registration.objects.filter(blood_group=bloodgroup,
                                                             state=state,
                                                             city=city,
                                                             )
            context = {
                'donor_filter': donor_filter
            }

            return render(request, 'polls/search_list.html', context)

        print(forms.errors)

    context_form = {
        'forms': forms
    }

    return render(request, 'polls/search.html', context_form)


def search_info(request, donor_id):
    detail = donor_Registration.objects.get(id=donor_id)

    context = {
        'details': detail
    }

    return render(request, 'polls/search_info.html', context)


def contact(request):
    forms = Contact()
    if request.method == 'POST':
        forms = Contact(request.POST)
        if forms.is_valid():
            forms.save()

    context = {
        'forms': forms
    }

    return render(request, 'polls/contact.html', context)


def donor_history(request, donor_id):
    donor = donor_Registration.objects.get(id=donor_id)
    donations = DonationHistory.objects.filter(donor=donor).order_by('-donation_date')
    
    context = {
        'donor': donor,
        'donations': donations,
    }
    return render(request, 'polls/donor_history.html', context)


def check_eligibility(request, donor_id):
    donor = donor_Registration.objects.get(id=donor_id)
    is_eligible, message = donor.is_eligible()
    
    # Calculate age
    today = date.today()
    age = today.year - donor.date_of_birth.year - ((today.month, today.day) < (donor.date_of_birth.month, donor.date_of_birth.day))
    
    context = {
        'donor': donor,
        'is_eligible': is_eligible,
        'message': message,
        'age': age,
    }
    return render(request, 'polls/eligibility_check.html', context)


@login_required
def record_donation(request, donor_id):
    donor = donor_Registration.objects.get(id=donor_id)
    
    if request.method == 'POST':
        form = DonationHistoryForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = donor
            donation.save()
            messages.success(request, 'Donation recorded successfully!')
            return redirect('donor_history', donor_id=donor.id)
    else:
        form = DonationHistoryForm()
    
    context = {
        'donor': donor,
        'form': form,
    }
    return render(request, 'polls/record_donation.html', context)


def blood_availability(request):
    print("Blood availability view called")  # Debug print
    form = BloodAvailabilityFilter(request.GET or None)
    blood_inventory = BloodInventory.objects.all()
    print(f"Blood inventory count: {blood_inventory.count()}")  # Debug print
    
    if form.is_valid():
        print("Form is valid")  # Debug print
        blood_group = form.cleaned_data.get('blood_group')
        min_quantity = form.cleaned_data.get('min_quantity')
        expiry_date = form.cleaned_data.get('expiry_date')
        status = form.cleaned_data.get('status')
        
        if blood_group:
            blood_inventory = blood_inventory.filter(blood_group=blood_group)
        if min_quantity:
            blood_inventory = blood_inventory.filter(quantity__gte=min_quantity)
        if expiry_date:
            blood_inventory = blood_inventory.filter(expiry_date__gte=expiry_date)
        if status:
            blood_inventory = blood_inventory.filter(status=status)
    
    # Calculate summary statistics
    total_units = blood_inventory.count()
    total_quantity = sum(inventory.quantity for inventory in blood_inventory)
    expiring_soon = blood_inventory.filter(
        expiry_date__lte=date.today() + timedelta(days=7)
    ).count()
    
    print(f"Total units: {total_units}, Total quantity: {total_quantity}, Expiring soon: {expiring_soon}")  # Debug print
    
    context = {
        'form': form,
        'blood_inventory': blood_inventory,
        'total_units': total_units,
        'total_quantity': total_quantity,
        'expiring_soon': expiring_soon,
    }
    
    return render(request, 'polls/blood_availability.html', context)


def donor_profile(request, donor_id):
    donor = donor_Registration.objects.get(id=donor_id)
    donations = DonationHistory.objects.filter(donor=donor).order_by('-donation_date')
    
    # Calculate next eligible donation date (typically 56 days after last donation)
    next_eligible_date = None
    if donor.last_donate_date:
        next_eligible_date = donor.last_donate_date + timedelta(days=56)
    
    # Handle profile update form
    if request.method == 'POST':
        # Get only the fields that can be updated
        donor.weight = request.POST.get('weight', donor.weight)
        donor.any_disease = request.POST.get('any_disease', '') == 'on'
        donor.allergies = request.POST.get('allergies', '') == 'on'
        donor.cardiac = request.POST.get('cardiac', '') == 'on'
        donor.bleeding_disorder = request.POST.get('bleeding_disorder', '') == 'on'
        donor.hbsAg_hcv_hIV = request.POST.get('hbsAg_hcv_hIV', '') == 'on'
        donor.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('donor_profile', donor_id=donor.id)
    
    # Health tips
    health_tips = [
        "Eat iron-rich foods before donation: spinach, beans, and lean meats.",
        "Stay hydrated: drink plenty of fluids before and after donation.",
        "Avoid strenuous physical activity for 24 hours after donation.",
        "Have a healthy meal before donating blood.",
        "Get a good night's sleep before donation day.",
        "Avoid alcohol for 24 hours before donation."
    ]
    
    context = {
        'donor': donor,
        'donations': donations,
        'next_eligible_date': next_eligible_date,
        'health_tips': health_tips,
        'today': date.today(),
    }
    
    return render(request, 'polls/donor_profile.html', context)


def all_donors(request):
    donors = donor_Registration.objects.all().order_by('name')
    
    # Filter by blood group if requested
    blood_group = request.GET.get('blood_group', '')
    if blood_group:
        donors = donors.filter(blood_group=blood_group.lower())
    
    context = {
        'donors': donors,
        'blood_group': blood_group,
        'blood_groups': [
            'a+', 'a-', 'b+', 'b-', 'ab+', 'ab-', 'o+', 'o-'
        ]
    }
    return render(request, 'polls/all_donors.html', context)