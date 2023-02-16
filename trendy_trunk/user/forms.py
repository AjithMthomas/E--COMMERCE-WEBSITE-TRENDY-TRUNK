from django import forms
from accounts.models import Account,UserProfile


# class

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':("image feild only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields =('address_line_1','address_line_2','city','state','country','postcode','profile_picture')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'