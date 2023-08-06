from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Account, UserAccount, TeamInvitation
from django.views.generic import FormView, View
from .forms import CustomInviteForm
from invitations.forms import InviteForm
from invitations.utils import get_invitation_model



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
        user_account = UserAccount.objects.create(
            user=self.request.user,
            account=self.object
        )
        user_account.save()
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('homepage')



# Description: Send email invitation
class SendInviteView(FormView):
    template_name = "invitations/forms/_invite.html"
    form_class = InviteForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            user_account = UserAccount.objects.get(user=self.request.user)
            team_invitation = TeamInvitation.objects.create(
                invited_email=email, 
                invited_by_user=self.request.user,
                account=user_account.account)
            team_invitation.save()
            
            
            invite = form.save(email)
            invite.inviter = self.request.user
            invite.save()
            invite.send_invitation(self.request)
        except Exception:
            return self.form_invalid(form)
        return self.render_to_response(
            self.get_context_data(
                success_message=("%(email)s has been invited") % {"email": email},
            ),
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
