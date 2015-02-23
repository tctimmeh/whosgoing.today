from django.db.models import Model, CharField


class Attendance(Model):
    name = CharField(max_length=10, unique=True)

    UNDECIDED = 1
    ACCEPT = 2
    REGRET = 3

    def __str__(self):
        return self.name
