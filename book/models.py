import decimal

from accounts.models import User
from core import model


class Listing(model.AbstractBaseModel):
    name = model.CharField(max_length=100)
    user = model.ForeignKey(User, on_delete=model.PROTECT, related_name='list')


class Room(model.AbstractBaseModel):
    name = model.CharField(max_length=100)
    is_vip = model.BooleanField(default=False)
    room_number = model.PositiveSmallIntegerField(unique=True)
    bed_count = model.PositiveSmallIntegerField(default=1)
    size = model.PositiveSmallIntegerField(default=20)
    has_good_view = model.BooleanField(default=False)
    description = model.TextField(null=True, blank=True)
    listing = model.ForeignKey(Listing, on_delete=model.CASCADE, related_name='room')

    def __str__(self):
        return f'{self.room_number}'

    def save(self, *args, **kwargs):
        if 5 < self.size >= (self.bed_count * 2 + 3):
            super().save(*args, **kwargs)
        else:
            raise ValueError('size must be up to 5 meters and gte bed_count *2 +3 meters')


class BookRoom(model.AbstractBaseModel):
    room = model.ForeignKey(Room, on_delete=model.PROTECT, related_name='book_room')
    start_at = model.DateTimeField()
    end_at = model.DateTimeField()
    price = model.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'room {self.room.room_number} in {self.start_at.date()}'

    def is_available(self):
        return not BookRoom.objects.filter(is_active=True, room=self.room).filter(
            model.Q(start_at__lte=self.start_at, end_at__gte=self.end_at) |
            model.Q(start_at__lte=self.start_at, end_at__lte=self.end_at, end_at__gt=self.start_at) |
            model.Q(start_at__gte=self.start_at, end_at__gte=self.end_at, start_at__lt=self.end_at) |
            model.Q(start_at__gte=self.start_at, end_at__lte=self.end_at)).exists()

    def save(self, *args, **kwargs):
        if self.start_at >= self.end_at:
            raise ValueError('started time cant be gte ended time')
        if self.is_available():
            super().save(*args, **kwargs)
        else:
            raise ValueError(f"reserved this room from {self.start_at} to {self.end_at}")


class BookedRoom(model.AbstractBaseModel):
    user = model.ForeignKey(User, on_delete=model.PROTECT, related_name='booked_room')
    book_room = model.ForeignKey(BookRoom, on_delete=model.PROTECT, related_name='booked_room')

    def save(self, *args, **kwargs):
        if not BookedRoom.objects.filter(book_room=self.book_room).exists():
            super().save(*args, **kwargs)
        else:
            raise ValueError('this room booked before')

    def __str__(self):
        return f'{self.user.username} booked {self.book_room.room.room_number}'
