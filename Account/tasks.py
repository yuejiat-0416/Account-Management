from celery import shared_task
from invitations.utils import get_invitation_model

# dummy HttpRequest object that simulates an actual 
# request without coming from a real user interaction
class FauxRequest:
    def __init__(self, url):
        self.url = url
    
    def build_absolute_uri(self, *args, **kwargs):
        return self.url


@shared_task
def send_invitation_task(invite_id, scheme, domain):
    Invitation = get_invitation_model()
    try:
        invite = Invitation.objects.get(id=invite_id)
        # Build the invite URL here
        base_url = f"{scheme}://{domain}"
        invite_url = f"{base_url}/invitations/accept-invite/{invite.key}"
        
        # If the send_invitation method requires the invite_url as an argument
        faux_request = FauxRequest(invite_url)
        invite.send_invitation(faux_request)

    except Invitation.DoesNotExist:
        print(f"No Invitation found for ID: {invite_id}")