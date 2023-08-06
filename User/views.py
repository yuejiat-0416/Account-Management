from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from Account.models import UserAccount

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'User/dashboard.html', {'section': 'dashboard'})


class JoinAccountView(CreateView):
    template_name = "user/join_account"
    model = UserAccount
    fields = "__all__"
    
    # 通过TeamInvitations里的invited email去调account，完成新用户的UserAccount Set up
    def form_valid(self, form):
        return super().form_valid(form)