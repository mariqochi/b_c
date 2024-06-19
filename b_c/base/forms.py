
# from django.forms import ModelForm
# from .models import Customer
    
# class CustomerForm(ModelForm):
#     class Meta:
#         model = Customer
#         fields = '__all__'

from django import forms
#from django.contrib.auth.models import User
from django.forms import ModelForm
#from .models import Customer
from django.core.exceptions import ValidationError
from .models import  Booking


from django import forms  # Change: Added import for forms
  # Change: Added import for User model
from .models import  Car, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']
 
 
 
 
 


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        






class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'loc_from', 'loc_to']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date must be after start date.")

        return cleaned_data

# class UserForm(forms.ModelForm):  # Change: Added UserForm for handling user registration
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email']

#     def clean_password2(self):  # Change: Added password validation method
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2



# class UserForm(ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password2']


# class CustomerForm(ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['first_name', 'last_name', 'phone', 'email',  'profile_pic']


# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['start_date', 'end_date']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

