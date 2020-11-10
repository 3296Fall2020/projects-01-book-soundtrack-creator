from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.index, name="index"),
    path("book_selector/", views.book_selector, name="book_selector"),
    path("set_user_info/", views.set_user_info, name = "set_user_info"),
    path("book_emotion_classifier/<id>", views.book_emotion_classifier, name = "book emotion classifier")
]