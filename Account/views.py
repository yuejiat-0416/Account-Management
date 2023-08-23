# django
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import FormView
from django.views.generic.edit import UpdateView

# Account model & forms
from .models import Account, UserAccount, TeamInvitation, UserRole, Role
from .forms import CustomInviteForm, AccountInformationForm

# django invitations
from invitations.forms import InviteForm
from invitations.utils import get_invitation_model
from invitations.views import SendInvite

# Celery task
from Account.tasks import send_invitation_task

# utils
from .utils import check_company_name_existence

Invitation = get_invitation_model()

# Description: For logged-in user to register their company information
class CreateAccountView(CreateView):
    template_name = "account/create_account.html"
    model = Account
    # fields = "__all__"
    fields = ["company_name", "company_size_range", "account_status"]
    # form_class = AccountForm
    
    def form_valid(self, form):
        company_name = form.cleaned_data.get('company_name')
        if check_company_name_existence(company_name):
            form.add_error('company_name', 'This company name already exists.')
            return self.form_invalid(form)

        self.object = form.save()
        admin_role = Role.objects.get(role_name="admin")
        user_account = UserAccount.objects.create(user = self.request.user, account = self.object)
        user_role = UserRole.objects.create(user=self.request.user, role=admin_role)
        user_account.save()
        messages.success(self.request, "Successfully Create Company!")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('homepage')


class UpdateAccountInformationView(UpdateView):
    template_name = 'account/update_account_information.html'
    model = Account
    form_class = AccountInformationForm
    
    def get_object(self):
        user_account_relation = UserAccount.objects.filter(user=self.request.user).first()
        if user_account_relation:
            return user_account_relation.account
        return None
    
    def get_success_url(self):
        return reverse_lazy('homepage')  
    def form_valid(self, form):
        # Print cleaned data to inspect it before saving
        print("Cleaned Data: ", form.cleaned_data)

        # Get the object you are about to update (optional)
        account_object = self.get_object()

        if account_object:
            # Manually update fields if needed
            account_object.company_facebook = form.cleaned_data.get('company_facebook')
            account_object.company_linkedin = form.cleaned_data.get('company_linkedin')
            account_object.company_twitter = form.cleaned_data.get('company_twitter')
            # Save the object but don't commit to the database yet
            account_object.save()

            # Print the new data for the object
            print(f"New object data: {account_object.__dict__}")

            # Print the entire saved object and its fields (optional)
            for field in account_object._meta.fields:
                print(f"{field.name}: {getattr(account_object, field.name)}")
            
            messages.success(self.request, "Account information updated successfully.")
        else:
            messages.error(self.request, "No associated account found.")
        
        return super().form_valid(form)

        
        return super().form_valid(form)





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
        print(user_account)
        print(user_account.account)
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

            # not use celery
            # invite = Invitation.create(email, inviter=self.request.user)
            # invite.send_invitation(self.request)
            
            scheme = 'https' if self.request.is_secure() else 'http'
            domain = self.request.get_host()
            invite = Invitation.create(email,  inviter=self.request.user)
            send_invitation_task.delay(invite.id, scheme, domain)

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
