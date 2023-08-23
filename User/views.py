# django 
from .models import CustomUser
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

# django-allauth
from allauth.account.views import SignupView

# django-invitations
from Account.models import UserAccount, UserRole
from Account.models import TeamInvitation, UserAccount

# utils
from .utils import get_company_name, get_employer_profile_detail

class CustomRegistrationView(SignupView):
    def get(self, request, *args, **kwargs):
        print("Custom registration view accessed via GET")
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        print("Custom registration view accessed via POST")
        return super().post(request, *args, **kwargs)
    
    
    '''
    To-do: Check if the registration happened through an invitation link
            if so: set the role according to the TeamInvitation instance.
    '''
    def form_valid(self, form):
        # Use the original behavior of the registration to save the user
        response = super().form_valid(form)
        # Check if the registration happened through an invitation link
        email = form.cleaned_data.get("email")
        try:
            invitation = TeamInvitation.objects.get(invited_email=email, is_accepted=False)

            # Create a UserAccount object linking the new user to the company
            UserAccount.objects.create(user = self.user, account = invitation.account)
            UserRole.objects.create(user=self.user, role=invitation.role)

            # Mark the invitation as used
            invitation.is_accepted = True
            invitation.save()
            
        except ObjectDoesNotExist:
            print('Register Error: TeamInvitation matching query does not exist')
        except Exception as e:
            # catch any other exceptions
            print('Another error occurred: ' + str(e))
            return self.form_invalid(form)
        
        return response

    def get_success_url(self):
        # default django allauth account login  
        return reverse('account_login') 

# TODO: change to class view
@login_required
def dashboard(request):
    user_account = UserAccount.objects.filter(user=request.user).first()
    company = get_company_name(request.user)
    info = get_employer_profile_detail(request.user)
    user_role = UserRole.objects.filter(user=request.user).first()
    role = None;
    if user_role:
        role = user_role.role.role_name

    members_roles = {}
    if company:
        company_instance = user_account.account
        members = CustomUser.objects.filter(user_account__account=company_instance)
        for member in members:
            roles = UserRole.objects.filter(user=member).values_list('role__role_name', flat=True)
            members_roles[member] = list(roles)


    context = {
        'section': 'dashboard',
        'company': company,
        'role': role,
        'members_roles': members_roles,
        'info': info,
    }


    return render(request, 'User/dashboard.html', context)