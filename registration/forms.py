from django import forms
from .models import student, contact  # Import the models in lowercase

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = student
        fields = ['name', 'dob', 'dept', 'course', 'yo_add', 'skill', 'area_int']  # Add fields relevant to the student model

class StudentContactEditForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['email', 'adr', 'pin', 'dist', 'st', 'gua_ph', 'f_name', 'm_name']  # Use only fields from the contact model
