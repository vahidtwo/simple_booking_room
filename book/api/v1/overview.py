from django.db.models import Avg
from django.http import HttpResponse
from rest_framework.views import APIView

from comment.models import Comment
from comment.serializer import CommentSerializer
from core.http import JsonResponse


class OverviewAPI(APIView):
    def get(self, request, id):
        comment = Comment.objects.select_related('booked_room__book_room__room').filter(
            booked_room__book_room__room_id=id)
        data = CommentSerializer(comment, exclude=('room_rate',), many=True).data
        room_rate = Comment.objects.select_related('booked_room__room').filter(
            booked_room__book_room__room_id=id).aggregate(room_rate=Avg('rate'))['room_rate']
        if request.query_params.get('return') == 'txt':
            comments_body = ',\n'.join([c.body + ' from ' + c.booked_room.user.username for c in comment])
            if comment.count():
                return HttpResponse(f"""this room got {comment.count()} comment and {room_rate} avg score have this.
                overviews:\n {comments_body}""")
            return HttpResponse("this room haven't any comment")
        return JsonResponse(data=data, extra={'room_rate': room_rate})
