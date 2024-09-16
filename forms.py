from django import forms
from .models import Employee, Department, Position, Country
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'image',
            'empcode',
            'name',
            'department',
            'position',
            'gender',
            'country',
            'email',
            'start',
            'dob',
            'workplace',
        ]
        labels = {
            'image': 'Image',
            'empcode': 'Employee Code',
            'name': 'Name',
            'department': 'Department',
            'position': 'Position',
            'gender': 'Gender',
            'country': 'Country',
            'email': 'Email',
            'start': 'Start',
            'dob': 'Date of Birth',
            'workplace': 'Workplace',
        }
        widgets = {
            'department': forms.Select(),
            'position': forms.Select(),
            'gender': forms.Select(),
            'country': forms.Select(),
            'email': forms.EmailInput(),
            'start': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'workplace': forms.Select(),
        }
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'parent',)
        labels = {
            'name': 'Department',
            'parent': 'Parent Department'
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('name',)
        labels = {'name': 'Position'}

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('name',)
        labels = {'name': 'Nationality'}