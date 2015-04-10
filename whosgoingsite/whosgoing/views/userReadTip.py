from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from whosgoing.models import UserReadTip
from zinnia.models import Entry


class UserReadTipView(View):
    def post(self, *args, **kwargs):
        next = self.request.POST.get('next')
        entry_id = self.request.POST.get('entry_id')
        if not next or not entry_id:
            raise PermissionDenied()

        entry = get_object_or_404(Entry, id=entry_id)

        UserReadTip.objects.update_or_create(user=self.request.user, entry=entry)
        return HttpResponseRedirect(self.request.POST['next'])

userReadTipView = login_required(UserReadTipView.as_view())
