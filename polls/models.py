from django.db import models
from datetime import date, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


class donor_Registration(models.Model):

    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    father_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        choices=gender_choices,
    )

    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True
    )

    phone_number = models.IntegerField(
        blank=True,
        null=True,
    )

    state = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    occupation = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    blood_group_choices = [
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b', 'B'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    ]

    blood_group = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=blood_group_choices,
    )

    home_address = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    last_donate_date = models.DateField(
        blank=True,
        null=True,
    )

    any_diseases_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    any_disease = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=any_diseases_choices,
    )

    allergies_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    allergies = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=allergies_choices,
    )

    cardiac_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    cardiac = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=cardiac_choices,
    )

    bleeding_disorder_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    bleeding_disorder = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=bleeding_disorder_choices,
    )

    hbsAg_hcv_hIV_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    hbsAg_hcv_hIV = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=hbsAg_hcv_hIV_choices,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(45.0), MaxValueValidator(200.0)],
        help_text="Weight in kg (minimum 45kg required for donation)"
    )
    
    donation_count = models.IntegerField(
        default=0,
        help_text="Number of times donated"
    )

    def is_eligible(self):
        # Calculate age
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        
        # Basic eligibility criteria
        if age < 18 or age > 65:
            return False, "Age must be between 18 and 65 years"
        
        if self.weight and self.weight < 45:
            return False, "Weight must be at least 45kg"
        
        if self.any_disease == 'yes' or self.allergies == 'yes' or self.cardiac == 'yes' or self.bleeding_disorder == 'yes' or self.hbsAg_hcv_hIV == 'yes':
            return False, "Medical conditions make you ineligible"
        
        # Check time since last donation (minimum 56 days)
        if self.last_donate_date:
            days_since_last_donation = (today - self.last_donate_date).days
            if days_since_last_donation < 56:
                return False, f"Must wait {56 - days_since_last_donation} more days before next donation"
        
        return True, "Eligible to donate"

    def __str__(self):
        return self.name


class sea_rch(models.Model):

    blood_group_choices = [
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b', 'B'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    ]

    blood_group = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=blood_group_choices,
    )

    state = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )


class con_tact(models.Model):

    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    phone_number = models.IntegerField(
        blank=True,
        null=True,
    )

    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True
    )

    subject = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class DonationHistory(models.Model):
    donor = models.ForeignKey(donor_Registration, on_delete=models.CASCADE, related_name='donations')
    donation_date = models.DateField(auto_now_add=True)
    blood_volume = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=450.0,
        help_text="Blood volume in ml"
    )
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Update donor's last donation date and count
        self.donor.last_donate_date = self.donation_date
        self.donor.donation_count += 1
        self.donor.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.donor.name} - {self.donation_date}"


class BloodInventory(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    COMPONENT_TYPES = [
        ('whole_blood', 'Whole Blood'),
        ('red_cells', 'Red Cells'),
        ('platelets', 'Platelets'),
        ('plasma', 'Plasma'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('expired', 'Expired'),
    ]

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    quantity = models.PositiveIntegerField(help_text="Quantity in milliliters")
    donation_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    donor = models.ForeignKey(donor_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Blood Inventory"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_blood_group_display()} {self.get_component_type_display()} - {self.quantity}ml"

    def is_expired(self):
        return self.expiry_date < date.today()

    def is_expiring_soon(self, days=7):
        return self.expiry_date <= date.today() + timedelta(days=days)
