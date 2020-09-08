from django.urls import path

from comment.api.v1 import CommentAPI

urlpatterns = [
    path('room/<int:id>/', CommentAPI.as_view()),
    path('<int:id>/', CommentAPI.as_view()),
    path('', CommentAPI.as_view())
]
