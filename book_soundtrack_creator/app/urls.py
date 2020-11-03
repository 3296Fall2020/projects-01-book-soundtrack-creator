from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.index, name="index"),
    path("/book_selector", views.book_selector, name="book_selector")
]