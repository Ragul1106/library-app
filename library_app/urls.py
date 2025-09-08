from django.urls import path
from . import views

app_name = "library_app"

urlpatterns = [
    # HTML views (CBV)
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/add/", views.BookCreateView.as_view(), name="book_add"),
    path("books/<int:pk>/edit/", views.BookUpdateView.as_view(), name="book_edit"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),

    # Author FBV
    path("api/authors/", views.author_list_create, name="author_list_create"),

    # API for books
    path("api/books/", views.BookListCreateAPI.as_view(), name="book_list_create_api"),
    path("api/books/<int:pk>/", views.BookRetrieveUpdateDeleteAPI.as_view(), name="book_detail_api"),
]
