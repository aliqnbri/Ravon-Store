from django import forms 
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# Register, Login, Edit 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
            }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            }
        
    def clean_password_2(self):
        '''
        Verify both passwords and phone Number.
        '''
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password  and password != password2:
            raise forms.ValidationError(_("Your passwords must match"))
        
        return password2    
    
    def save(self, commit=True):
        '''Save the provided password in hashed format'''
        user = super(CustomUserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
