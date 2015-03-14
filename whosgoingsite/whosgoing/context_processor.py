from whosgoing.models import Invitation


def whosgoing(request):
    invitations = Invitation.objects.for_user(request.user)
    if invitations:
        invitations = invitations.order_by('event__name')

    return {
        'invitations': invitations
    }
