from django import forms
from .models import Doctors, patients
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User



TYPE_SELECT = [
        ('female', 'Female'),
        ('male', 'Male')
]
STATUS_SELECT = [
        ('inactive', 'Inactive'),
        ('active', 'Active')
]


STATE=[
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'),
    ('05', '05'),
    ('06', '06'),
    ('07', '07')
]
class DoctorsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.Meta.required:
            self.fields[key].required = False
    
    dob = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={
                'class': 'form-control datetimepicker',
                'type': 'text'
                },
            format='%Y-%m-%d'
        )
    )
    
    class Meta:
        model = Doctors
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'dob',
            'gender',
            'address',
            'country',
            'city',
            'state',
            'postalcode',
            'phone',
            'photo',
            'bio',
            'status',
            'expertise'
            
        ]
        required = [
            'first_name',
            'last_name',
            'username',
            'email',
            'dob',
            'gender',
            'address',
            'country',
            'city',
            'state',
            'postalcode',
            'phone',
            'photo',
            'bio',
            'status',
            'expertise'
            
        ]

       
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
                
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'email'
            }),
            
            'gender': forms.Select(choices=TYPE_SELECT, attrs={
                'class': 'form-check-input'
              
            
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
                
            }),
            'country': forms.Select(attrs={
                'class': 'form-control select'
            }),
            
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
                
            }),
            'state': forms.Select(choices=STATE, attrs={
                'class': 'form-control select'
                
            }),
            

            'postalcode': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'number'
                
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'number'
                
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'accept': "image/*",
                'id': 'uploadPhoto'
                
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control summernote',
                'type': 'text',
                'rows': "5", 
                'cols': "30",
                'style': 'resize:none;'
                
            }),
            'status': forms.Select(choices=STATUS_SELECT, attrs={
                'class': 'form-check-inline'
              
                
                
            }),
            'expertise': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            })

        }

class UsercreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.Meta.required:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]
        required = [
            'first_name',
            'last_name',
            'username',
            'email'
            
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'email'
                
            })

        }

class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.Meta.required:
            self.fields[key].required = True
    
    dob = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={
                'class': 'form-control datetimepicker',
                'type': 'text'
                },
            format='%Y-%m-%d'
        )
    )
    
    class Meta:
        model = patients
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'dob',
            'gender',
            'address',
            'country',
            'city',
            'state',
            'postalcode',
            'phone',
            'photo',
            'symptom',
            'status'
            
            
        ]
        required = [
            'first_name',
            'last_name',
            'username',
            'email',
            'dob',
            'gender',
            'address',
            'country',
            'city',
            'state',
            'postalcode',
            'phone',  
            'status',
            'symptom'
            
            
        ]

       
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
                
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'email'
            }),
            
            'gender': forms.Select(choices=TYPE_SELECT, attrs={
                'class': 'form-check-input'
              
            
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
                
            }),
            'country': forms.Select(attrs={
                'class': 'form-control select'
            }),
            
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
                
            }),
            'state': forms.Select(choices=STATE, attrs={
                'class': 'form-control select'
                
            }),
            

            'postalcode': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'number'
                
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'number'
                
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'accept': "image/*"
                
            }),
            
            'status': forms.Select(choices=STATUS_SELECT, attrs={
                'class': 'form-check-inline'
              
                
                
            }),
                'symptom': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            })

        }



