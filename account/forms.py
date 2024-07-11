from django import forms 
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# Register, Login, Edit 

class RegisterUserForm (forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    # phone_number = forms.CharField(max_length=13,required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password',]

    def clean_password_2(self):
        '''
        Verify both passwords and phone Number.
        '''
        
        password = self.cleaned_data.get("password")
        password_2 = self.cleaned_data.get("password_2")
        if password  and password != password_2:
            raise forms.ValidationError(_("Your passwords must match"))
        
        return password_2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterUserForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class EditUserForm(forms.ModelForm):
    """
    A form for editing existing users.
    """
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True  # Make email field read-only

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user