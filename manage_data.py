import os
import sys
import django
import json
import random
from datetime import datetime, timedelta
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from doctors.models import Doctor
from listings.models import Subject, Listing

fake = Faker()

class DataManager:
    def __init__(self):
        self.data_dir = "sample_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("          MANAGE DATA TOOL")
        print("="*50)
        print("1. Clear Data")
        print("2. Export Data")
        print("3. Import Data")
        print("4. Generate Data")
        print("5. Exit")
        print("="*50)
        
    def clear_data(self):
        """Clear all sample data from database"""
        print("\nClearing all sample data...")
        try:
            # Clear in correct order to avoid foreign key constraints
            Listing.objects.all().delete()
            Subject.objects.all().delete()
            Doctor.objects.all().delete()
            print("✓ All sample data cleared successfully!")
        except Exception as e:
            print(f"✗ Error clearing data: {e}")
            
    def export_data(self):
        """Export current data to JSON files with complete relationships"""
        print("\nExporting data to JSON files...")
        
        try:
            # Export Doctors
            doctors_data = []
            for doctor in Doctor.objects.all():
                doctors_data.append({
                    'id': doctor.id,
                    'name': doctor.name,
                    'description': doctor.description,
                    'phone': doctor.phone,
                    'email': doctor.email,
                    'is_mvp': doctor.is_mvp,
                    'hire_date': doctor.hire_date.isoformat() if doctor.hire_date else None
                })
            
            with open(f'{self.data_dir}/doctors.json', 'w') as f:
                json.dump(doctors_data, f, indent=2)
            print(f"✓ Exported {len(doctors_data)} doctors")
            
            # Export Subjects
            subjects_data = []
            for subject in Subject.objects.all():
                subjects_data.append({
                    'id': subject.id,
                    'name': subject.name
                })
            
            with open(f'{self.data_dir}/subjects.json', 'w') as f:
                json.dump(subjects_data, f, indent=2)
            print(f"✓ Exported {len(subjects_data)} subjects")
            
            # Export Listings with complete relationship data
            listings_data = []
            for listing in Listing.objects.all():
                listing_data = {
                    'id': listing.id,
                    'doctor_id': listing.doctor.id if listing.doctor else None,
                    'title': listing.title,
                    'address': listing.address,
                    'district': listing.district,
                    'description': listing.description,
                    'service': listing.service,
                    'room_type': listing.room_type,
                    'screen': listing.screen,
                    'professional': listing.professional,
                    'rooms': listing.rooms,
                    'is_published': listing.is_published,
                    'list_date': listing.list_date.isoformat() if listing.list_date else None,
                    'professionals_ids': [prof.id for prof in listing.professionals.all()]
                }
                listings_data.append(listing_data)
            
            with open(f'{self.data_dir}/listings.json', 'w') as f:
                json.dump(listings_data, f, indent=2)
            print(f"✓ Exported {len(listings_data)} listings")
            
            print("✓ All data exported successfully!")
            
        except Exception as e:
            print(f"✗ Error exporting data: {e}")
            import traceback
            traceback.print_exc()
            
    def import_data(self):
        """Import data from JSON files with proper relationship handling"""
        print("\nImporting data from JSON files...")
        
        try:
            # Track created objects for relationships
            doctor_id_map = {}
            subject_id_map = {}
            
            # Import Doctors first
            if os.path.exists(f'{self.data_dir}/doctors.json'):
                with open(f'{self.data_dir}/doctors.json', 'r') as f:
                    doctors_data = json.load(f)
                
                for doctor_data in doctors_data:
                    doctor, created = Doctor.objects.get_or_create(
                        email=doctor_data['email'],
                        defaults={
                            'name': doctor_data['name'],
                            'description': doctor_data['description'],
                            'phone': doctor_data['phone'],
                            'is_mvp': doctor_data['is_mvp']
                        }
                    )
                    # Store mapping from old ID to new ID
                    doctor_id_map[doctor_data['id']] = doctor.id
                print(f"✓ Imported {len(doctors_data)} doctors")
            
            # Import Subjects
            if os.path.exists(f'{self.data_dir}/subjects.json'):
                with open(f'{self.data_dir}/subjects.json', 'r') as f:
                    subjects_data = json.load(f)
                
                for subject_data in subjects_data:
                    subject, created = Subject.objects.get_or_create(
                        name=subject_data['name']
                    )
                    # Store mapping from old ID to new ID
                    subject_id_map[subject_data['id']] = subject.id
                print(f"✓ Imported {len(subjects_data)} subjects")
            
            # Import Listings last (depends on Doctors and Subjects)
            if os.path.exists(f'{self.data_dir}/listings.json'):
                with open(f'{self.data_dir}/listings.json', 'r') as f:
                    listings_data = json.load(f)
                
                imported_listings = 0
                for listing_data in listings_data:
                    # Find the corresponding doctor using our mapping
                    doctor_id = listing_data.get('doctor_id')
                    if doctor_id and doctor_id in doctor_id_map:
                        try:
                            doctor = Doctor.objects.get(id=doctor_id_map[doctor_id])
                            
                            # Create or get the listing
                            listing, created = Listing.objects.get_or_create(
                                title=listing_data['title'],
                                doctor=doctor,
                                defaults={
                                    'address': listing_data['address'],
                                    'district': listing_data['district'],
                                    'description': listing_data['description'],
                                    'service': listing_data['service'],
                                    'room_type': listing_data['room_type'],
                                    'screen': listing_data['screen'],
                                    'professional': listing_data['professional'],
                                    'rooms': listing_data['rooms'],
                                    'is_published': listing_data['is_published']
                                }
                            )
                            
                            # Handle ManyToMany relationship for professionals
                            professionals_ids = listing_data.get('professionals_ids', [])
                            valid_subject_ids = []
                            for old_subject_id in professionals_ids:
                                if old_subject_id in subject_id_map:
                                    valid_subject_ids.append(subject_id_map[old_subject_id])
                            
                            if valid_subject_ids:
                                subjects = Subject.objects.filter(id__in=valid_subject_ids)
                                listing.professionals.set(subjects)
                            
                            imported_listings += 1
                            
                        except Doctor.DoesNotExist:
                            print(f"  Warning: Doctor with ID {doctor_id} not found for listing '{listing_data['title']}'")
                        except Exception as e:
                            print(f"  Warning: Error creating listing '{listing_data['title']}': {e}")
                    else:
                        print(f"  Warning: No valid doctor ID for listing '{listing_data['title']}'")
                
                print(f"✓ Imported {imported_listings} listings")
            
            print("✓ All data imported successfully!")
            
        except Exception as e:
            print(f"✗ Error importing data: {e}")
            import traceback
            traceback.print_exc()
            
    def generate_sample_data(self):
        """Generate comprehensive sample data"""
        print("\nGenerating sample data...")
        
        # Sample data lists
        medical_specialties = [
            'Cardiology', 'Dermatology', 'Neurology', 'Pediatrics', 'Oncology',
            'Orthopedics', 'Psychiatry', 'Radiology', 'Surgery', 'Gynecology'
        ]
        
        districts = ['Central', 'Western', 'Eastern', 'Southern', 'Northern']
        room_types = ['Single', 'Double', 'Suite', 'Executive', 'Standard']
        services_range = list(range(1, 11))
        screen_range = list(range(1, 6))
        professional_range = list(range(1, 8))
        rooms_range = ['1', '2', '3', '4', '5+']
        
        # Realistic phone number formats
        phone_formats = ['###-###-####', '(###)###-####', '+1-###-###-####']
        
        try:
            # Create Subjects
            subjects = []
            for specialty in medical_specialties:
                subject, created = Subject.objects.get_or_create(name=specialty)
                subjects.append(subject)
            print(f"✓ Created {len(subjects)} subjects")
            
            # Create Doctors
            doctors = []
            for i in range(25):
                # Generate phone number that fits in 20 characters
                phone = fake.numerify(text=random.choice(phone_formats))
                if len(phone) > 20:
                    phone = phone[:20]
                
                doctor = Doctor.objects.create(
                    name=fake.name(),
                    description=fake.text(max_nb_chars=200),
                    phone=phone,
                    email=fake.unique.email(),
                    is_mvp=fake.boolean(chance_of_getting_true=30),
                    hire_date=fake.date_between(start_date='-5y', end_date='today')
                )
                doctors.append(doctor)
            print(f"✓ Created {len(doctors)} doctors")
            
            # Create Listings
            listings = []
            for i in range(20):
                # Ensure title is not too long
                title = f"{fake.company()} Medical Center"
                if len(title) > 200:
                    title = title[:200]
                
                # Ensure address is not too long
                address = fake.address()
                if len(address) > 200:
                    address = address[:200]
                
                listing = Listing.objects.create(
                    doctor=random.choice(doctors),
                    title=title,
                    address=address,
                    district=random.choice(districts),
                    description=fake.text(max_nb_chars=300),
                    service=random.choice(services_range),
                    room_type=random.choice(room_types),
                    screen=random.choice(screen_range),
                    professional=random.choice(professional_range),
                    rooms=random.choice(rooms_range),
                    is_published=fake.boolean(chance_of_getting_true=80),
                    list_date=fake.date_time_between(start_date='-1y', end_date='now')
                )
                
                # Add random professionals (2-4 subjects)
                num_professionals = random.randint(2, 4)
                listing.professionals.set(random.sample(subjects, num_professionals))
                listings.append(listing)
            print(f"✓ Created {len(listings)} listings")
            
            print("✓ Sample data generation completed successfully!")
            print(f"Total records created:")
            print(f"  - Doctors: {len(doctors)}")
            print(f"  - Subjects: {len(subjects)}")
            print(f"  - Listings: {len(listings)}")
            
        except Exception as e:
            print(f"✗ Error generating sample data: {e}")
            import traceback
            traceback.print_exc()
            
    def run(self):
        """Main program loop"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                confirm = input("Are you sure you want to clear all data? (y/n): ")
                if confirm.lower() == 'y':
                    self.clear_data()
                else:
                    print("Operation cancelled.")
                    
            elif choice == '2':
                self.export_data()
                
            elif choice == '3':
                self.import_data()
                
            elif choice == '4':
                confirm = input("This will generate new sample data. Continue? (y/n): ")
                if confirm.lower() == 'y':
                    self.generate_sample_data()
                else:
                    print("Operation cancelled.")
                    
            elif choice == '5':
                print("Thank you for using Manage Data Tool. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1-5.")
                
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    manager = DataManager()
    manager.run()