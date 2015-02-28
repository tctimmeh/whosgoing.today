from django.db.models import Model, CharField


class Attendance(Model):
    name = CharField(max_length=10, unique=True)

    UNDECIDED = 1
    ACCEPT = 2
    REGRET = 3

    def __str__(self):
        return self.name

    @classmethod
    def from_string(cls, name):
        name = name.upper()
        if name == 'ACCEPT':
            return Attendance(id=Attendance.ACCEPT)
        elif name == 'REGRET':
            return Attendance(id=Attendance.REGRET)
        elif name == 'UNDECIDED':
            return Attendance(id=Attendance.UNDECIDED)
        else:
            raise ValueError('{} is not a valid attendance string'.format(name))

