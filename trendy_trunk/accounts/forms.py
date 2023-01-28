from django import forms
from . models import Account

class Registrationform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password']
    

    #  for checking the password and confirm password are equal
    def clean(self):
        cleaned_data=super(Registrationform,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password !=confirm_password:
            raise forms.ValidationError("entered passwords deos not match each other!")
    