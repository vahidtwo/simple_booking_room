from django.db.models import Avg

from accounts.serializer import UserSerializer
from booked.serializer import BookedRoomSerializer
from comment.models import Comment
from core import serializers


class CommentSerializer(serializers.ModelSerializer):
    room_rate = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    booked_room = BookedRoomSerializer(exclude=('user',))

    def update(self, instance, validated_data):
        instance.rate = validated_data.get('rate', instance.rate)
        instance.body = validated_data.get('body', instance.body)
        instance.title = validated_data.get('title', instance.title)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ['rate', 'title', 'body', 'user', 'room_rate', 'booked_room']

    def get_room_rate(self, obj):
        return Comment.objects.select_related('booked_room__room').filter(
            booked_room__room_id=obj.booked_room.room.id).aggregate(room_rate=Avg('rate'))['room_rate']

    def get_user(self, obj):
        return UserSerializer(obj.booked_room.user).data
