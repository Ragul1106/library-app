from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework import generics
from django.http import JsonResponse
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# ---------- CBV for Book CRUD ----------
class BookListView(ListView):
    model = Book
    template_name = "library_app/book_list.html"
    context_object_name = "books"


class BookDetailView(DetailView):
    model = Book
    template_name = "library_app/book_detail.html"


class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "genre", "published_year"]
    template_name = "library_app/book_form.html"
    success_url = reverse_lazy("library_app:book_list")


class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", "author", "genre", "published_year"]
    template_name = "library_app/book_form.html"
    success_url = reverse_lazy("library_app:book_list")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "library_app/book_confirm_delete.html"
    success_url = reverse_lazy("library_app:book_list")


# ---------- FBV for Author (list + create) ----------
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def author_list_create(request):
    if request.method == "GET":
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# ---------- DRF API for Books ----------
class BookListCreateAPI(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        author_name = self.request.query_params.get("author")
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
        return queryset


class BookRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
