from accounts.models import User
from booked.models import Room, BookedRoom
from core import model


class Comment(model.AbstractBaseModel):
    title = model.CharField(max_length=200)
    body = model.TextField()
    rate = model.PositiveSmallIntegerField(
        choices=((0, '-'), (1, "*"), (2, "**"), (3, "***"), (4, "****"), (5, "*****")), default=3)
    booked_room = model.OneToOneField(BookedRoom, on_delete=model.CASCADE, related_name='comment')

    def __str__(self):
        return f'{self.title} from {self.booked_room.user.username}'