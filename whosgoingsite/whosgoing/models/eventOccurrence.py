from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, DateTimeField, ManyToManyField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from whosgoing.models import Event


class EventOccurrence(Model):
    event = ForeignKey(Event, related_name='occurrences')
    time = DateTimeField(default=timezone.now)
    members = ManyToManyField(User, through='OccurrenceMember')

    def __str__(self):
        return '{} occurrence at {}'.format(self.event.name, self.time)

    @property
    def is_past(self):
        return self.time < timezone.now()

    @property
    def member_details_by_user(self):
        from whosgoing.models import OccurrenceMember
        return OccurrenceMember.objects.filter(occurrence=self).order_by('user__username')

    def add_member(self, user):
        from whosgoing.models import OccurrenceMember
        OccurrenceMember.objects.create(user=user, occurrence=self)

    def remove_member(self, user):
        from whosgoing.models import OccurrenceMember
        OccurrenceMember.objects.filter(occurrence=self, user=user).delete()

@receiver(post_save, sender=EventOccurrence)
def event_occurrence_post_save(sender, instance, created, raw, **kwargs):
    if not created or raw:
        return
    eventMembers = instance.event.members.all()
    [instance.add_member(member) for member in eventMembers]
