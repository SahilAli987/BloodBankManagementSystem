from django.core.management.base import BaseCommand
from polls.models import BloodInventory, BloodGroup, ComponentType
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Sets up demo data for blood inventory'

    def handle(self, *args, **options):
        # Clear existing inventory data
        BloodInventory.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing blood inventory data'))
        
        # Get all blood groups and component types
        blood_groups = BloodGroup.objects.all()
        component_types = ComponentType.objects.all()
        
        if not blood_groups.exists():
            self.stdout.write(self.style.ERROR('No blood groups found. Please create blood groups first.'))
            return
            
        if not component_types.exists():
            self.stdout.write(self.style.ERROR('No component types found. Please create component types first.'))
            return
        
        # Status options
        statuses = ['Available', 'Reserved', 'Expired', 'Used']
        
        # Create random inventory entries
        inventory_entries = []
        today = timezone.now().date()
        
        for _ in range(50):  # Create 50 random entries
            blood_group = random.choice(blood_groups)
            component_type = random.choice(component_types)
            quantity = random.randint(200, 450)  # in ml
            
            # Random collection date between 35 days ago and today
            days_ago = random.randint(0, 35)
            collection_date = today - timedelta(days=days_ago)
            
            # Set expiry date based on component type (example logic)
            if component_type.name == 'Red Blood Cells':
                # RBCs typically last 42 days
                expiry_date = collection_date + timedelta(days=42)
            elif component_type.name == 'Platelets':
                # Platelets typically last 5 days
                expiry_date = collection_date + timedelta(days=5)
            elif component_type.name == 'Plasma':
                # Plasma can last up to a year when frozen
                expiry_date = collection_date + timedelta(days=365)
            else:
                # Default expiry of 35 days for other components
                expiry_date = collection_date + timedelta(days=35)
            
            # Set status based on expiry date
            if expiry_date < today:
                status = 'Expired'
            else:
                # For non-expired items, randomly assign a status
                status = random.choices(
                    ['Available', 'Reserved', 'Used'],
                    weights=[0.7, 0.2, 0.1],
                    k=1
                )[0]
            
            # Create the inventory entry
            inventory_entry = BloodInventory(
                blood_group=blood_group,
                component_type=component_type,
                quantity=quantity,
                collection_date=collection_date,
                expiry_date=expiry_date,
                status=status
            )
            inventory_entries.append(inventory_entry)
        
        # Bulk create all entries
        BloodInventory.objects.bulk_create(inventory_entries)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(inventory_entries)} blood inventory entries')
        ) 