from django.forms import ModelForm
from .models import Account, UserAccount, TeamInvitation
from django import forms

       
        
class CustomInviteForm(forms.Form):
    email = forms.EmailField(
        label=("email"),
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"}),
        initial="",
    )

    
    
    