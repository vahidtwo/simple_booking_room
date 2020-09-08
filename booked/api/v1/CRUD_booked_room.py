import datetime

from rest_framework import status
from rest_framework.views import APIView

from accounts.models import User
from booked.models import BookedRoom, Room
from booked.serializer import BookedRoomSerializer
from core.http import JsonResponse


class BookedRoomAPI(APIView):
    def get(self, request, id):
        try:
            return JsonResponse(data=BookedRoomSerializer(BookedRoom.objects.get(pk=id)).data)
        except BookedRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - booked-room does not exists')

    def post(self, request):
        try:
            data = request.data
            booked_room = BookedRoom()
            booked_room.room = Room.objects.get(room_number=data['room_number'])
            booked_room.user = User.objects.get(pk=data['user_id'])
            date_format = '%Y-%m-%d %H:%M:%S'
            booked_room.start_at = datetime.datetime.strptime(data['start_at'], date_format)
            booked_room.end_at = datetime.datetime.strptime(data['end_at'], date_format)
            booked_room.save()
            return JsonResponse(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - user not found')
        except Room.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - Room not found')
        except Exception as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, message=str(e))

    def delete(self, request, id):
        try:
            BookedRoom.objects.get(pk=id).delete()
            return JsonResponse(message='delete successful')
        except BookedRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - booked-room does not exists')

    def put(self, request, id):
        try:
            data = dict(request.data)
            booked_room = BookedRoom.objects.get(pk=id)
            try:
                user = User.objects.get(pk=data.get('user_id'))
            except User.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - user does not exists')
            try:
                room = Room.objects.get(room_number=data.get('room_number'))
            except Room.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - room does not exists')
            ser = BookedRoomSerializer(booked_room, data)
            if ser.is_valid():
                a = ser.save(user=user, room=room)
                return JsonResponse(message='update successful')
            else:
                return JsonResponse(message=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except BookedRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - booked-room does not exists')


