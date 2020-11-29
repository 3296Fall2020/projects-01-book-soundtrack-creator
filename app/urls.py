from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.index, name="index"),
    path("book_selector/", views.book_selector, name="book_selector"),
    path("set_user_info/", views.set_user_info, name = "set_user_info"),
    path("book_info/<id>", views.book_info, name = "book emotion classifier"),
    path("login/", views.login, name = "login"),
    path("initial_sign_in/", views.initial_sign_in , name="initial_sign_in"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("book_import/", views.book_import, name = "book_import"),
    path("book_import_upload/", views.book_import_upload, name = "book_import_upload"),
    path("book_upload/", views.book_upload, name = "book_upload"),
    path("find_books/", views.find_books, name = "find books"),
    path("test/", views.test, name = "testing"),
    path("get_book/<id>", views.get_book, name = "get book"),
    path("profile/", views.profile, name = "profile"),
    path("logout/", views.logout, name = "logout"),
]