from django import forms
from myapp.models import SocietyDeatils


class SocietyForm(forms.ModelForm):
    class Meta:
        model = SocietyDeatils
        fields = ['email', 'phone_no', 'contact_name', 'society_name', 'society_address', 'city', 'pin_code', 'state',
                  'country', 'society_registration_number']
        widgets = {'email': forms.TextInput(attrs={'class': 'form-control'}),
                   'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
                   'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'society_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'society_address': forms.TextInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
                   'state': forms.TextInput(attrs={'class': 'form-control'}),
                   'country': forms.TextInput(attrs={'class': 'form-control'}),
                   'society_registration_number': forms.TextInput(attrs={'class': 'form-control'})
                   }
