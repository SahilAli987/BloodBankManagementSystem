from django.core.management.base import BaseCommand
from polls.models import BloodInventory
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Initialize sample blood inventory data'

    def handle(self, *args, **kwargs):
        # Clear existing inventory
        BloodInventory.objects.all().delete()
        
        # Create sample data
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        statuses = ['available', 'reserved', 'expired']
        
        today = date.today()
        
        # Create 24 inventory items (3 for each blood group)
        for blood_group in blood_groups:
            # Available with future expiry
            BloodInventory.objects.create(
                blood_group=blood_group,
                quantity=450,
                donation_date=today - timedelta(days=5),
                expiry_date=today + timedelta(days=30),
                status='available'
            )
            
            # Available but expiring soon
            BloodInventory.objects.create(
                blood_group=blood_group,
                quantity=350,
                donation_date=today - timedelta(days=25),
                expiry_date=today + timedelta(days=5),
                status='available'
            )
            
            # Reserved
            BloodInventory.objects.create(
                blood_group=blood_group,
                quantity=300,
                donation_date=today - timedelta(days=10),
                expiry_date=today + timedelta(days=20),
                status='reserved'
            )
        
        # Add a few expired items for testing
        for bg in ['A+', 'O+', 'B+']:
            BloodInventory.objects.create(
                blood_group=bg,
                quantity=400,
                donation_date=today - timedelta(days=45),
                expiry_date=today - timedelta(days=5),
                status='expired'
            )
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {BloodInventory.objects.count()} inventory items')) 