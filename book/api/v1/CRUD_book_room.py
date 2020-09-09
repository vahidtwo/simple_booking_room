import datetime

from rest_framework import status, viewsets
from rest_framework.views import APIView

from accounts.models import User
from book.models import BookRoom, Room, BookedRoom, Listing
from book.serializer import BookRoomSerializer, ListingSerializer
from core.http import JsonResponse


class BookRoomAPI(APIView):
    def get(self, request, id):
        try:
            return JsonResponse(data=BookRoomSerializer(BookRoom.objects.get(pk=id)).data)
        except BookRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - book-room does not exists')

    def post(self, request):
        try:
            data = request.data
            booked_room = BookRoom()
            booked_room.room = Room.objects.get(room_number=data['room_number'])
            date_format = '%Y-%m-%d %H:%M:%S'
            booked_room.start_at = datetime.datetime.strptime(data['start_at'], date_format)
            booked_room.end_at = datetime.datetime.strptime(data['end_at'], date_format)
            booked_room.price = data['price']
            booked_room.save()
            return JsonResponse(status=status.HTTP_201_CREATED)
        except Room.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - Room not found')
        except Exception as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, message=str(e))

    def delete(self, request, id):
        try:
            BookRoom.objects.get(pk=id).delete()
            return JsonResponse(message='delete successful')
        except BookRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - book-room does not exists')

    def put(self, request, id):
        try:
            data = dict(request.data)
            booked_room = BookRoom.objects.get(pk=id)
            try:
                room = Room.objects.get(room_number=data.get('room_number'))
            except Room.DoesNotExist:
                room = None
            ser = BookRoomSerializer(booked_room, data, partial=True)
            if ser.is_valid():
                if room:
                    ser.save(room=room)
                else:
                    ser.save()
                return JsonResponse(message='update successful')
            else:
                return JsonResponse(message=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except BookRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - book-room does not exists')


class BookedRoomAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            booked_room = BookedRoom()
            booked_room.user = User.objects.get(pk=data['user_id'])
            booked_room.book_room = BookRoom.objects.get(pk=data['book_room_id'])
            booked_room.save()
            return JsonResponse(status=status.HTTP_201_CREATED, message='create successful')
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - user not found')
        except BookRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - bookroom not found')
        except ValueError as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, message=str(e))

    def get(self, request):
        """ get all non booked room"""
        try:
            date_format = '%Y-%m-%d'
            start_at = datetime.datetime.strptime(request.query_params['start_at'], date_format)
            end_at = datetime.datetime.strptime(request.query_params['end_at'], date_format)
            book_room = BookRoom.objects.filter(booked_room__isnull=True, start_at__date__gte=start_at,
                                                end_at__date__lte=end_at)
            data = BookRoomSerializer(book_room, many=True).data
            return JsonResponse(data=data)
        except Exception as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, message=str(e))

    def delete(self, request, id):
        try:
            BookedRoom.objects.get(pk=id).delete()
            return JsonResponse(message='delete successful')
        except BookedRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - booked room not found')


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
