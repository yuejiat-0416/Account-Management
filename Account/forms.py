from django.forms import ModelForm
from .models import Account, UserAccount, TeamInvitation
from django import forms
from .models import Role
from invitations.forms import InviteForm


class CustomInviteForm(InviteForm):
    
    role = forms.ChoiceField(
        choices=Role.ROLE_TYPE_CHOICES,
        required=True,
    )
    
    def save(self, email, role):
        return TeamInvitation.objects.create(invited_email=email, role=role)

    
    

    
    
    