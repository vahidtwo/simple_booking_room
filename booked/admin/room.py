from core.admin import AbstractBaseAdmin


class RoomAdmin(AbstractBaseAdmin):
    list_display = ('id', 'room_number', 'has_good_view', 'is_vip', 'bed_count', 'size')
    list_editable = ('bed_count', 'size')
    search_fields = ('id', 'room_number')
    list_filter = ('is_vip', 'has_good_view')
