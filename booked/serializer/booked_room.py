import datetime

from accounts.serializer import UserSerializer
from booked.models import BookedRoom
from booked.serializer.room import RoomSerializer
from core import serializers


class BookedRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer(exclude=('priority', 'is_active', 'created_at', 'updated_at', 'description'), read_only=True)
    user = UserSerializer(read_only=True)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.room = validated_data.get('room', instance.room)
        instance.start_at = validated_data.get('start_at')
        instance.end_at = validated_data.get('end_at')
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    class Meta:
        model = BookedRoom
        fields = '__all__'
