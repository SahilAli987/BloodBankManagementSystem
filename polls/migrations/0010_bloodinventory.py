# Generated by Django 3.2 on 2025-04-09 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20250409_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('component_type', models.CharField(choices=[('whole_blood', 'Whole Blood'), ('red_cells', 'Red Cells'), ('platelets', 'Platelets'), ('plasma', 'Plasma')], max_length=20)),
                ('quantity', models.PositiveIntegerField(help_text='Quantity in milliliters')),
                ('donation_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('status', models.CharField(choices=[('available', 'Available'), ('reserved', 'Reserved'), ('expired', 'Expired')], default='available', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.donor_registration')),
            ],
            options={
                'verbose_name_plural': 'Blood Inventory',
                'ordering': ['-created_at'],
            },
        ),
    ]
