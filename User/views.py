# django 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# django-allauth
from allauth.account.views import SignupView

# django-invitations
from Account.models import UserAccount
from Account.models import TeamInvitation, UserAccount



class CustomRegistrationView(SignupView):
    def get(self, request, *args, **kwargs):
        print("Custom registration view accessed via GET")
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        print("Custom registration view accessed via POST")
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        # Use the original behavior of the registration to save the user
        response = super().form_valid(form)

        # Check if the registration happened through an invitation link
        email = form.cleaned_data.get("email")
        try:
            invitation = TeamInvitation.objects.get(invited_email=email, is_accepted=False)

            # Create a UserAccount object linking the new user to the company
            UserAccount.objects.create(
                user=self.user,
                account=invitation.account
            )

            # Mark the invitation as used
            invitation.is_accepted = True
            invitation.save()
            
        except Exception as e:
            print('Register Error: ' + str(e))
            return self.form_invalid(form)
        
        return response

    def get_success_url(self):
        return reverse('account_login')

@login_required
def dashboard(request):
    user_account = UserAccount.objects.filter(user=request.user).first()
    company = None
    if user_account:
        company = user_account.account.company_name

    context = {
        'section': 'dashboard',
        'company': company
    }

    return render(request, 'User/dashboard.html', context)