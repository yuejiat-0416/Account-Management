from Account.models import UserAccount, UserRole, Account
# get the name of the company
def get_company_name(user):
    user_account = UserAccount.objects.filter(user=user).first()
    if user_account:
        return user_account.account.company_name
    return None

# get employer profile detail 
# company email, name, summary, industry, size, website, location, domain,
# linkedin, facebook, twitter, video, etc
from django.shortcuts import get_object_or_404

def get_employer_profile_detail(user):
    # Assuming the Account model has a OneToOneField with the User model
    # and is accessible via the attribute `account`
    account = get_object_or_404(Account, user_account__user=user)
    
    profile_detail = {
        'company_name': account.company_name,
        'company_size_range': account.company_size_range,
        'company_facebook': account.company_facebook,
        'company_linkedin': account.company_linkedin,
        'company_twitter': account.company_twitter,
    }
    return profile_detail
