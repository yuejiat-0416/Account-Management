# django
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import FormView

# Account model & forms
from .models import Account, UserAccount, TeamInvitation, UserRole, Role
from .forms import CustomInviteForm

# django invitations
from invitations.forms import InviteForm
from invitations.utils import get_invitation_model
from invitations.views import SendInvite

# Celery task
from Account.tasks import send_invitation_task

Invitation = get_invitation_model()

# Description: For logged-in user to register their company information
class CreateAccountView(CreateView):
    template_name = "account/create_account.html"
    model = Account
    # fields = "__all__"
    fields = ["company_name", "company_size_range", "account_status"]
    # form_class = AccountForm
    
    def form_valid(self, form):
        self.object = form.save()
        admin_role = Role.objects.get(role_name="admin")
        user_account = UserAccount.objects.create(user = self.request.user, account = self.object)
        user_role = UserRole.objects.create(user=self.request.user, role=admin_role)
        user_account.save()
        messages.success(self.request, "Successfully Create Company!")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('homepage')

# Description: Send email invitation
class SendInviteView(FormView):
    template_name = "invitations/forms/_invite.html"
    form_class = CustomInviteForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        role_type = form.cleaned_data["role"]
        role = Role.objects.get(role_type=role_type)

        user_account = UserAccount.objects.filter(user=self.request.user).first()
        if not user_account:
            # If user_account doesn't exist, log the error and handle the response.
            print('SendInviteView Error: UserAccount for user {user} does not exist'.format(user=self.request.user))
            return self.form_invalid(form)
        
        # If user_account exists, continue with the invitation process
        try:
            # Store the invitation in the database
            team_invitation = TeamInvitation.objects.create(
                invited_email=email, 
                invited_by_user=self.request.user,
                account=user_account.account,
                role=role)
            team_invitation.save()
# email-invitation
            
            invite = Invitation.create(email, inviter=self.request.user)
            invite.send_invitation(self.request)
# 

            invite = form.save(email) 
            invite.inviter = self.request.user
            invite.save()
            # invite.send_invitation(self.request)
# celery

            # schedule the task to run in the background with Celery
            scheme = 'https' if self.request.is_secure() else 'http'
            send_invitation_task.delay(invite.id, scheme, self.request.get_host())
            
        except Exception as e:
            print('SendInviteView Error: ' + str(e))
            return self.form_invalid(form)
        
        messages.success(self.request, "Successfully Invite a New User!")
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self) -> str:
        return reverse_lazy('homepage')
    
    
# Each instance of Roles should be created by the site admin?
