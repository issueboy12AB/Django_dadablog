from django.urls import path

from . import views

urlpatterns = [
    path('<str:author_id>', views.TopicViews.as_view()),
]