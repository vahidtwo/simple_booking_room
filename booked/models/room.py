from core import model


class Room(model.AbstractBaseModel):
    is_vip = model.BooleanField(default=False)
    room_number = model.PositiveSmallIntegerField(unique=True)
    bed_count = model.PositiveSmallIntegerField(default=1)
    size = model.PositiveSmallIntegerField(default=20)
    has_good_view = model.BooleanField(default=False)
    price_per_min = model.FloatField(default=0.5)
    description = model.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.room_number}'

    def save(self, *args, **kwargs):
        if self.price_per_min < 0:
            raise ValueError('price cant be negative')
        if 5 < self.size >= (self.bed_count * 2 + 3) and self.bed_count >= 0:
            super().save(*args, **kwargs)
        else:
            raise ValueError('size must be up to 5 meters and gte bed_count *2 +3 meters')
