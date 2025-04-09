# Blood Bank Management System

A comprehensive web application for managing blood donations, donors, and blood inventory. This system helps blood banks efficiently track donations, manage donor information, monitor blood availability, and ensure proper inventory management.

## Features

- **Donor Management**
  - Register new donors with detailed health information
  - Track donor donation history
  - Check donor eligibility for donations
  - Donor profile management
  - Search for donors by blood group, location, etc.

- **Blood Inventory Management**
  - Track available blood units by blood group
  - Monitor expiry dates of blood units
  - Filter blood inventory by various parameters
  - Summary statistics for available blood units
  - Status tracking (available, reserved, expired)

- **Donation Recording**
  - Record new blood donations from registered donors
  - Track donation volumes and dates
  - Maintain detailed notes for each donation

- **User Interface**
  - Responsive, modern UI built with Bootstrap
  - Intuitive filtering and search functionality
  - Clear visual indicators for blood status and availability

## Technologies Used

- **Backend**: Django (Python web framework)
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Django's built-in authentication system

## How to Run the App

### Create a virtual environment

Download python & pip

### Download requirement file

```
$ pip install -r requirement.txt
```

Then run migrations and create an admin user:

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

### Start the app

```
$ python manage.py runserver
```

Open browser, http://localhost:8000

### Stop the app

Press `Ctrl+C` in the terminal

## Usage Guide

1. **Admin Panel**
   - Access the admin panel at http://localhost:8000/admin/
   - Use the superuser credentials created earlier
   - Manage all aspects of the system from the admin interface

2. **Donor Registration**
   - Register new donors with health information
   - The system automatically checks eligibility based on health data

3. **Blood Inventory**
   - View and filter blood availability
   - Track units that are expiring soon
   - Monitor total blood quantity by blood group

4. **Search Functionality**
   - Find donors by blood group, location
   - Search through blood inventory

5. **Donor Profiles**
   - View donor history
   - Check eligibility status
   - Record new donations 