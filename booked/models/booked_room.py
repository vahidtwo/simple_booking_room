from accounts.models import User
from booked.models.room import Room
from core import model


class BookedRoom(model.AbstractBaseModel):
    room = model.ForeignKey(Room, on_delete=model.PROTECT, related_name='booked_room')
    start_at = model.DateTimeField()
    end_at = model.DateTimeField()
    user = model.ForeignKey(User, on_delete=model.PROTECT, related_name='booked_room')
    price = model.FloatField(editable=False)

    def __str__(self):
        return f'room {self.room.room_number} for {self.user.username} in {self.start_at.date()}'

    def is_available(self):
        return not BookedRoom.objects.filter(room=self.room).filter(
            model.Q(start_at__lte=self.start_at, end_at__gte=self.end_at) |
            model.Q(start_at__lte=self.start_at, end_at__lte=self.end_at, end_at__gt=self.start_at) |
            model.Q(start_at__gte=self.start_at, end_at__gte=self.end_at, start_at__lt=self.end_at) |
            model.Q(start_at__gte=self.start_at, end_at__lte=self.end_at)).exists()

    def save(self, *args, **kwargs):
        if self.start_at >= self.end_at:
            raise ValueError('started time cant be gte ended time')
        reserved_time = self.end_at - self.start_at
        self.price = self.room.price_per_min * (reserved_time.total_seconds() // 60)
        if self.is_available():
            super().save(*args, **kwargs)
        else:
            raise ValueError(f"user {self.user.username} reserved this room from {self.start_at} to {self.end_at}")
