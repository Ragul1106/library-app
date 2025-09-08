from rest_framework import serializers
from datetime import datetime
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    book_age = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "author", "genre", "published_year", "book_age"]

    def get_book_age(self, obj):
        return datetime.now().year - obj.published_year

    def validate_published_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio"]
