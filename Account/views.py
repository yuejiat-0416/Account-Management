# django
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import FormView

# Account model
from .models import Account, UserAccount, TeamInvitation

# django invitations
from invitations.forms import InviteForm
from invitations.utils import get_invitation_model

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
        user_account = UserAccount.objects.create(user = self.request.user, account = self.object)
        user_account.save()
        messages.success(self.request, "Successfully Create Company!")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('homepage')

# Description: Send email invitation
class SendInviteView(FormView):
    template_name = "invitations/forms/_invite.html"
    # template_name = "User/dashboard.html"

    form_class = InviteForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]

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
                account=user_account.account)
            team_invitation.save()

            invite = form.save(email) 
            invite.inviter = self.request.user
            invite.save()
            # invite.send_invitation(self.request)

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
