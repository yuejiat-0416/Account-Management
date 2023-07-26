from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
   
   
User = get_user_model()

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    # field_order = ['email', 'username', ...]
    
    class Meta:
        model = User
        
    '''  
    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
    '''