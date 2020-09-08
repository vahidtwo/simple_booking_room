from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import User
from booked.models import BookedRoom
from comment.models import Comment
from comment.serializer.comment_serializer import CommentSerializer
from core.http import JsonResponse


class CommentAPI(APIView):
    def get(self, request, id):
        try:
            return JsonResponse(data=CommentSerializer(Comment.objects.get(pk=id)).data)
        except Comment.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message="wrong id - Comment not found")

    def post(self, request):
        try:
            data = request.data
            comment = Comment()
            comment.title = data.get('title')
            comment.body = data.get('body')
            comment.rate = data.get('rate')
            comment.booked_room = BookedRoom.objects.get(pk=data['booked_room_id'])
            comment.save()
            return JsonResponse(status=status.HTTP_201_CREATED, message='create successful')
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message="wrong id - user not found")
        except BookedRoom.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message="wrong id - booked_room not found")
        except IntegrityError:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, message='for a booked_room you can add one comment')

    def delete(self, request, id):
        try:
            Comment.objects.get(pk=id).delete()
            return JsonResponse(message='Comment deleted')
        except Comment.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message="wrong id - comment not found")

    def put(self, request, id):
        try:
            comment = Comment.objects.get(pk=id)
            data = dict(request.data)
            ser = CommentSerializer(comment, data, partial=True)
            if ser.is_valid():
                ser.save()
                return JsonResponse(message='Comment Updated')
            return JsonResponse(message=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message="wrong id - comment not found")
