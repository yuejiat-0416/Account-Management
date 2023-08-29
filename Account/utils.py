from .models import Account  # Adjust import as needed

def check_company_name_existence(company_name):
    return Account.objects.filter(company_name=company_name).exists()
